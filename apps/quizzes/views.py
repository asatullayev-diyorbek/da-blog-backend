import uuid
import random
from datetime import timedelta

from django.db import transaction
from django.db.models import Sum
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AnswerOption, Arena, ArenaParticipant, ArenaQuestion, PointTransaction, Question, Quiz, QuizAttempt, UserBadge, UserGamification
from .serializers import QuestionSerializer, QuizAttemptSerializer, QuizDetailSerializer, QuizListSerializer
from .services import award_arena_points, award_attempt_points


class QuizListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        quizzes = Quiz.objects.filter(published=True).select_related("lesson__course").prefetch_related("questions")
        return Response(QuizListSerializer(quizzes, many=True).data)


class ArenaQuestionPoolView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        topics = request.data.get("topics", [])
        try:
            count = int(request.data.get("count", 10))
        except (TypeError, ValueError):
            return Response({"detail": "Savollar soni noto'g'ri."}, status=400)
        if not isinstance(topics, list) or not topics:
            return Response({"detail": "Kamida bitta mavzu tanlang."}, status=400)
        if count < 10:
            return Response({"detail": "Arena uchun kamida 10 ta savol tanlanadi."}, status=400)
        count = min(count, 100)
        questions = list(Question.objects.filter(
            quiz__published=True,
            quiz__topic__in=topics,
        ).prefetch_related("options"))
        if len(questions) < count:
            return Response({"detail": f"Tanlangan mavzularda faqat {len(questions)} ta savol mavjud."}, status=400)
        random.shuffle(questions)
        return Response({
            "topics": topics,
            "count": count,
            "questions": QuestionSerializer(questions[:count], many=True).data,
        })


class ArenaCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        topics = request.data.get("topics", [])
        try:
            count = int(request.data.get("count", 10))
        except (TypeError, ValueError):
            return Response({"detail": "Savollar soni noto'g'ri."}, status=400)
        if not isinstance(topics, list) or not topics:
            return Response({"detail": "Kamida bitta mavzu tanlang."}, status=400)
        if count < 10:
            return Response({"detail": "Arena uchun kamida 10 ta savol tanlanadi."}, status=400)
        count = min(count, 50)

        questions = list(Question.objects.filter(
            quiz__published=True,
            quiz__topic__in=topics,
        ))
        if len(questions) < count:
            return Response({"detail": f"Tanlangan mavzularda faqat {len(questions)} ta savol mavjud."}, status=400)
        random.shuffle(questions)

        arena = Arena.objects.create(
            owner=request.user,
            topics=topics,
            question_count=count,
        )
        ArenaParticipant.objects.create(arena=arena, user=request.user, is_owner=True)
        ArenaQuestion.objects.bulk_create([
            ArenaQuestion(arena=arena, question=question, order=index)
            for index, question in enumerate(questions[:count], 1)
        ])

        return Response({
            "id": str(arena.id),
            "code": arena.code,
            "status": arena.status,
            "topics": arena.topics,
            "question_count": arena.question_count,
            "max_players": arena.max_players,
            "owner": request.user.username,
            "invite_path": f"/arena/{arena.code}",
        }, status=201)


def arena_payload(arena, request):
    participants = arena.participants.select_related("user").all()
    def avatar_url(user):
        if not user.avatar:
            return None
        avatar = user.avatar.url
        if avatar.startswith("http"):
            return avatar
        return request.build_absolute_uri(avatar) if request else f"{settings.MEDIA_URL}{avatar.lstrip('/')}"

    return {
        "id": str(arena.id),
        "code": arena.code,
        "status": arena.status,
        "topics": arena.topics,
        "question_count": arena.question_count,
        "max_players": arena.max_players,
        "owner_id": arena.owner_id,
        "owner_username": arena.owner.username,
        "participants": [{
            "id": item.user_id,
            "username": item.user.username,
            "full_name": item.user.telegram_full_name or item.user.get_full_name() or item.user.username,
            "avatar": avatar_url(item.user),
            "is_owner": item.is_owner,
            "score": item.score,
            "correct_answers": item.correct_answers,
            "rank": item.rank,
            "xp": {1: 100, 2: 60, 3: 30}.get(item.rank, 0) if arena.status == "finished" else 0,
            "xp_awarded": item.xp_awarded,
        } for item in participants],
        "invite_path": f"/arena/{arena.code}",
    }


class ArenaDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, code):
        arena = get_object_or_404(Arena.objects.select_related("owner"), code=code)
        return Response(arena_payload(arena, request))


class ArenaJoinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, code):
        arena = get_object_or_404(Arena.objects.select_related("owner"), code=code)
        if arena.status != "waiting":
            return Response({"detail": "Bu arena allaqachon boshlangan yoki yakunlangan."}, status=400)
        if arena.participants.count() >= arena.max_players and not arena.participants.filter(user=request.user).exists():
            return Response({"detail": "Arena ishtirokchilar bilan to'ldi."}, status=400)
        ArenaParticipant.objects.get_or_create(
            arena=arena,
            user=request.user,
            defaults={"is_owner": arena.owner_id == request.user.id},
        )
        return Response(arena_payload(arena, request))


class ArenaStartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, code):
        arena = get_object_or_404(Arena.objects.select_related("owner"), code=code)
        if arena.owner_id != request.user.id:
            return Response({"detail": "Arenani faqat egasi boshlashi mumkin."}, status=403)
        if arena.status != "waiting":
            return Response({"detail": "Arena holatini o'zgartirib bo'lmaydi."}, status=400)
        arena.status = "started"
        arena.started_at = timezone.now()
        arena.save(update_fields=["status", "started_at"])
        return Response(arena_payload(arena, request))


def finish_arena_if_needed(arena):
    if arena.status != "started" or not arena.started_at:
        return
    elapsed = (timezone.now() - arena.started_at).total_seconds()
    if elapsed < arena.question_count * arena.question_duration:
        return
    arena.status = "finished"
    arena.finished_at = timezone.now()
    arena.save(update_fields=["status", "finished_at"])
    participants = list(arena.participants.order_by("-score", "total_time", "joined_at"))
    for rank, participant in enumerate(participants, 1):
        participant.rank = rank
        participant.save(update_fields=["rank"])
    award_arena_points(arena)


def arena_game_payload(arena, participant, request=None):
    finish_arena_if_needed(arena)
    if arena.status == "finished":
        return {"status": "finished", "participants": arena_payload(arena, request)["participants"]}
    elapsed = max(0, int((timezone.now() - arena.started_at).total_seconds()))
    question_index = min(elapsed // arena.question_duration, arena.question_count - 1)
    remaining_seconds = arena.question_duration - (elapsed % arena.question_duration)
    arena_question = arena.questions.select_related("question").prefetch_related("question__options").get(order=question_index + 1)
    answered = participant.answers.filter(question=arena_question.question).exists()
    return {
        "status": arena.status,
        "question_index": question_index,
        "question_count": arena.question_count,
        "remaining_seconds": remaining_seconds,
        "answered": answered,
        "question": QuestionSerializer(arena_question.question).data,
        "participants": arena_payload(arena, request)["participants"],
    }


class ArenaGameView(APIView):
    permission_classes = [IsAuthenticated]

    def get_participant(self, arena, request):
        return get_object_or_404(ArenaParticipant, arena=arena, user=request.user)

    def get(self, request, code):
        arena = get_object_or_404(Arena, code=code)
        participant = self.get_participant(arena, request)
        if arena.status == "waiting":
            return Response({"status": "waiting", "participants": arena_payload(arena, request)["participants"]})
        return Response(arena_game_payload(arena, participant, request))

    @transaction.atomic
    def post(self, request, code):
        arena = get_object_or_404(Arena, code=code)
        participant = self.get_participant(arena, request)
        if arena.status != "started":
            return Response({"detail": "Arena hozir javob qabul qilmayapti."}, status=400)
        state = arena_game_payload(arena, participant, request)
        if state["status"] != "started":
            return Response(state)
        question_id = request.data.get("question_id")
        option_id = request.data.get("option_id")
        if int(question_id) != state["question"]["id"]:
            return Response({"detail": "Bu savol uchun vaqt tugagan."}, status=400)
        question = get_object_or_404(Question, id=question_id)
        option = get_object_or_404(AnswerOption, id=option_id, question=question)
        if ArenaAnswer.objects.filter(participant=participant, question=question).exists():
            return Response(state)
        response_time = arena.question_duration - state["remaining_seconds"]
        is_correct = option.is_correct
        points = (100 + state["remaining_seconds"]) if is_correct else 0
        ArenaAnswer.objects.create(
            arena=arena,
            participant=participant,
            question=question,
            selected_option=option,
            is_correct=is_correct,
            response_time=response_time,
            points=points,
        )
        participant.score += points
        participant.correct_answers += int(is_correct)
        participant.total_time += response_time
        participant.save(update_fields=["score", "correct_answers", "total_time"])
        return Response(arena_game_payload(arena, participant, request))


class QuizDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        quiz = get_object_or_404(
            Quiz.objects.filter(published=True).select_related("lesson__course").prefetch_related("questions__options"),
            slug=slug,
        )
        data = QuizDetailSerializer(quiz).data
        if quiz.randomize_questions:
            import random
            random.shuffle(data["questions"])
        return Response(data)


def get_guest_id(request):
    return request.headers.get("X-Guest-ID", "").strip()[:128] or str(uuid.uuid4())


class QuizStartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug, published=True)
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user=request.user if request.user.is_authenticated else None,
            guest_id="" if request.user.is_authenticated else get_guest_id(request),
            total_questions=quiz.questions.count(),
        )
        return Response({"attempt_id": str(attempt.id), "guest_id": attempt.guest_id, "started_at": attempt.started_at})


class QuizSubmitView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, attempt_id):
        attempt = get_object_or_404(
            QuizAttempt.objects.select_for_update().select_related("quiz"), id=attempt_id,
        )
        if attempt.completed_at:
            return Response(QuizAttemptSerializer(attempt).data)

        if attempt.user_id:
            if not request.user.is_authenticated or request.user.id != attempt.user_id:
                return Response({"detail": "Bu urinish sizga tegishli emas."}, status=403)
        elif attempt.guest_id != get_guest_id(request):
            return Response({"detail": "Guest sessiya mos kelmadi."}, status=403)

        submitted = request.data.get("answers", {})
        if not isinstance(submitted, dict):
            return Response({"answers": "answers obyekt ko'rinishida bo'lishi kerak."}, status=400)

        question_ids = set(attempt.quiz.questions.values_list("id", flat=True))
        answer_ids = {int(value) for value in submitted.values() if str(value).isdigit()}
        valid_options = AnswerOption.objects.filter(question_id__in=question_ids, id__in=answer_ids).select_related("question")
        selected = {str(option.question_id): option for option in valid_options}
        correct = sum(1 for question_id in question_ids if selected.get(str(question_id)) and selected[str(question_id)].is_correct)
        total = len(question_ids)
        score = round(correct * 100 / total) if total else 0

        attempt.answers = {str(key): value for key, value in submitted.items()}
        attempt.correct_answers = correct
        attempt.total_questions = total
        attempt.score = score
        attempt.passed = score >= attempt.quiz.pass_score
        attempt.completed_at = timezone.now()
        attempt.save(update_fields=["answers", "correct_answers", "total_questions", "score", "passed", "completed_at"])
        award_attempt_points(attempt)

        return Response(QuizAttemptSerializer(attempt).data)


class QuizAttemptView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, attempt_id):
        attempt = get_object_or_404(QuizAttempt.objects.select_related("quiz"), id=attempt_id)
        if attempt.user_id and (not request.user.is_authenticated or request.user.id != attempt.user_id):
            return Response({"detail": "Bu urinish sizga tegishli emas."}, status=403)
        if not attempt.user_id and attempt.guest_id != get_guest_id(request):
            return Response({"detail": "Guest sessiya mos kelmadi."}, status=403)
        return Response(QuizAttemptSerializer(attempt).data)


class ClaimGuestAttemptsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        guest_id = request.headers.get("X-Guest-ID", "").strip()[:128]
        if not guest_id:
            return Response({"detail": "Guest ID topilmadi."}, status=400)
        attempts = list(QuizAttempt.objects.filter(
            guest_id=guest_id,
            user__isnull=True,
            completed_at__isnull=False,
        ).select_related("quiz"))
        for attempt in attempts:
            attempt.user = request.user
            attempt.guest_id = ""
            attempt.save(update_fields=["user", "guest_id"])
            award_attempt_points(attempt)
        return Response({"claimed": len(attempts)})


class MyAttemptsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            attempts = QuizAttempt.objects.filter(user=request.user, completed_at__isnull=False)
        else:
            attempts = QuizAttempt.objects.filter(guest_id=get_guest_id(request), completed_at__isnull=False)
        attempts = attempts.select_related("quiz")
        return Response(QuizAttemptSerializer(attempts, many=True).data)


class GamificationMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = UserGamification.objects.get_or_create(user=request.user)
        badges = UserBadge.objects.filter(user=request.user).select_related("badge")
        return Response({
            "total_points": profile.total_points,
            "level": profile.level,
            "current_streak": profile.current_streak,
            "next_level_points": profile.level * 100,
            "badges": [{"code": item.badge.code, "name": item.badge.name, "description": item.badge.description, "icon": item.badge.icon, "earned_at": item.earned_at} for item in badges],
        })


class LeaderboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        period = request.query_params.get("period", "all")
        transactions = PointTransaction.objects.all()
        if period in ("week", "month"):
            days = 7 if period == "week" else 30
            transactions = transactions.filter(created_at__date__gte=timezone.localdate() - timedelta(days=days - 1))
        rows = list(transactions.values("user_id", "user__username", "user__first_name", "user__last_name", "user__telegram_full_name", "user__avatar").annotate(points=Sum("points")).order_by("-points", "user__username")[:100])
        user_rank = None
        result = []
        for index, row in enumerate(rows, 1):
            if request.user.is_authenticated and row["user_id"] == request.user.id:
                user_rank = index
            avatar = row["user__avatar"]
            if avatar and not avatar.startswith("http"):
                avatar = f"{settings.MEDIA_URL}{avatar.lstrip('/')}"
            full_name = row["user__telegram_full_name"] or " ".join(filter(None, [row["user__first_name"], row["user__last_name"]])) or row["user__username"]
            result.append({"rank": index, "username": row["user__username"], "full_name": full_name, "avatar": avatar, "points": row["points"], "is_me": request.user.is_authenticated and row["user_id"] == request.user.id})
        return Response({"period": period, "user_rank": user_rank, "results": result})
