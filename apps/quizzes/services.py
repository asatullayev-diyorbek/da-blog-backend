from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import Arena, Badge, PointTransaction, QuizAttempt, UserBadge, UserGamification


BADGES = {
    "first-test": ("Birinchi qadam", "Birinchi testni yakunladingiz.", "🚀"),
    "perfect-score": ("Mukammal natija", "Testni 100% natija bilan yakunladingiz.", "💯"),
    "streak-3": ("3 kunlik streak", "Uch kun ketma-ket faol bo'ldingiz.", "🔥"),
    "ten-tests": ("Faol o'quvchi", "10 ta testni yakunladingiz.", "🎓"),
}


def award_badge(user, code):
    name, description, icon = BADGES[code]
    badge, _ = Badge.objects.get_or_create(code=code, defaults={"name": name, "description": description, "icon": icon})
    UserBadge.objects.get_or_create(user=user, badge=badge)


@transaction.atomic
def award_attempt_points(attempt: QuizAttempt):
    if not attempt.user_id or PointTransaction.objects.filter(attempt=attempt).exists():
        return

    # Har bir user har bir quiz uchun XP'ni faqat birinchi yakunlangan
    # urinishda oladi. Keyingi urinishlar natija sifatida saqlanadi, ammo XP bermaydi.
    if QuizAttempt.objects.filter(
        user=attempt.user,
        quiz=attempt.quiz,
        completed_at__isnull=False,
    ).exclude(id=attempt.id).exists():
        return

    user = attempt.user
    profile, _ = UserGamification.objects.select_for_update().get_or_create(user=user)
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)
    points = 10
    if attempt.score >= 70:
        points += 20
    if attempt.score >= 90:
        points += 20
    if profile.last_activity_date == yesterday:
        profile.current_streak += 1
    elif profile.last_activity_date != today:
        profile.current_streak = 1

    if profile.total_points == 0:
        points += 50
    profile.total_points += points
    profile.level = profile.total_points // 100 + 1
    profile.last_activity_date = today
    profile.save(update_fields=["total_points", "level", "current_streak", "last_activity_date"])
    PointTransaction.objects.create(user=user, points=points, reason="Test yakunlandi", attempt=attempt)

    completed_count = QuizAttempt.objects.filter(user=user, completed_at__isnull=False).count()
    if completed_count == 1:
        award_badge(user, "first-test")
    if attempt.score == 100:
        award_badge(user, "perfect-score")
    if profile.current_streak >= 3:
        award_badge(user, "streak-3")
    if completed_count >= 10:
        award_badge(user, "ten-tests")


@transaction.atomic
def award_arena_points(arena: Arena):
    rewards = {1: 100, 2: 60, 3: 30}
    participants = list(arena.participants.select_for_update().select_related("user").order_by("rank", "id"))
    for participant in participants:
        points = rewards.get(participant.rank, 0)
        if not points or participant.xp_awarded:
            continue
        profile, _ = UserGamification.objects.select_for_update().get_or_create(user=participant.user)
        profile.total_points += points
        profile.level = profile.total_points // 100 + 1
        profile.last_activity_date = timezone.localdate()
        profile.save(update_fields=["total_points", "level", "last_activity_date"])
        PointTransaction.objects.create(user=participant.user, points=points, reason=f"Arena #{arena.code} — {participant.rank}-o'rin", arena=arena)
        participant.xp_awarded = True
        participant.save(update_fields=["xp_awarded"])
