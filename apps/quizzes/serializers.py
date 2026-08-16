import random

from rest_framework import serializers

from .models import AnswerOption, Question, Quiz, QuizAttempt


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ["id", "text", "order"]


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)
    code_bank = serializers.SerializerMethodField()

    def get_code_bank(self, obj):
        if obj.quiz.quiz_type != "code_fix":
            return []
        bank = [str(answer) for answer in (obj.code_answers or [])]
        random.shuffle(bank)
        return bank

    class Meta:
        model = Question
        fields = ["id", "text", "explanation", "order", "topic", "difficulty", "options", "code_template", "code_bank"]


class QuizListSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source="questions.count", read_only=True)
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    course_slug = serializers.CharField(source="lesson.course.slug", read_only=True)
    xp_reward = serializers.SerializerMethodField()

    def get_xp_reward(self, obj):
        return 50

    class Meta:
        model = Quiz
        fields = ["id", "title", "slug", "description", "lesson", "lesson_title", "course", "course_slug", "category", "topic", "quiz_type", "time_limit", "pass_score", "questions_count", "xp_reward"]


class QuizDetailSerializer(QuizListSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta(QuizListSerializer.Meta):
        fields = QuizListSerializer.Meta.fields + ["questions"]


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source="quiz.title", read_only=True)
    quiz_slug = serializers.CharField(source="quiz.slug", read_only=True)
    question_results = serializers.SerializerMethodField()

    def get_question_results(self, obj):
        def normalize(value):
            return " ".join(str(value or "").strip().split()).casefold()

        results = []
        for question in obj.quiz.questions.all():
            submitted = obj.answers.get(str(question.id), obj.answers.get(question.id)) if isinstance(obj.answers, dict) else None
            if obj.quiz.quiz_type == "code_fix":
                received = submitted if isinstance(submitted, list) else [submitted] if submitted is not None else []
                expected = [normalize(item) for item in (question.code_answers or [])]
                received = [normalize(item) for item in received]
                is_correct = len(received) == len(expected) and all(received[index] == item for index, item in enumerate(expected))
            else:
                selected = question.options.filter(id=submitted).first() if str(submitted).isdigit() else None
                is_correct = bool(selected and selected.is_correct)
            results.append({"question_id": question.id, "order": question.order, "is_correct": is_correct})
        return results

    class Meta:
        model = QuizAttempt
        fields = ["id", "quiz", "quiz_slug", "quiz_title", "score", "correct_answers", "total_questions", "passed", "started_at", "completed_at", "question_results"]
