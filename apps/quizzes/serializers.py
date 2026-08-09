from rest_framework import serializers

from .models import AnswerOption, Question, Quiz, QuizAttempt


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ["id", "text", "order"]


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "explanation", "order", "topic", "difficulty", "options"]


class QuizListSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source="questions.count", read_only=True)
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    course_slug = serializers.CharField(source="lesson.course.slug", read_only=True)
    xp_reward = serializers.SerializerMethodField()

    def get_xp_reward(self, obj):
        return 50

    class Meta:
        model = Quiz
        fields = ["id", "title", "slug", "description", "lesson", "lesson_title", "course", "course_slug", "category", "topic", "time_limit", "pass_score", "questions_count", "xp_reward"]


class QuizDetailSerializer(QuizListSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta(QuizListSerializer.Meta):
        fields = QuizListSerializer.Meta.fields + ["questions"]


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source="quiz.title", read_only=True)
    quiz_slug = serializers.CharField(source="quiz.slug", read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ["id", "quiz", "quiz_slug", "quiz_title", "score", "correct_answers", "total_questions", "passed", "started_at", "completed_at"]
