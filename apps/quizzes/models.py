import uuid

from django.db import models
from django.utils.text import slugify

from apps.courses.models import Lesson
from apps.courses.models import Course
from apps.users.models import User


def generate_arena_code():
    return uuid.uuid4().hex[:8].upper()


class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    description = models.TextField(blank=True, verbose_name="Tavsif")
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="quizzes", null=True, blank=True,
        verbose_name="Dars",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="quizzes", null=True, blank=True,
        verbose_name="Kurs",
    )
    category = models.CharField(max_length=100, blank=True, verbose_name="Kategoriya")
    topic = models.CharField(max_length=150, blank=True, verbose_name="Asosiy mavzu")
    time_limit = models.PositiveIntegerField(default=0, verbose_name="Vaqt limiti (soniya)")
    pass_score = models.PositiveSmallIntegerField(default=60, verbose_name="O'tish foizi")
    randomize_questions = models.BooleanField(default=False, verbose_name="Savollarni aralashtirish")
    published = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Test"
        verbose_name_plural = "Testlar"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Arena(models.Model):
    STATUS_CHOICES = [
        ("waiting", "Kutilmoqda"),
        ("started", "Boshlandi"),
        ("finished", "Yakunlandi"),
        ("cancelled", "Bekor qilindi"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=8, unique=True, default=generate_arena_code, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_arenas")
    topics = models.JSONField(default=list, blank=True)
    question_count = models.PositiveSmallIntegerField(default=10)
    question_duration = models.PositiveSmallIntegerField(default=20)
    max_players = models.PositiveSmallIntegerField(default=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting", db_index=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Arena"
        verbose_name_plural = "Arenalar"

    def __str__(self):
        return f"Arena {self.code}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(verbose_name="Savol")
    explanation = models.TextField(blank=True, verbose_name="Izoh")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Tartib")
    topic = models.CharField(max_length=150, blank=True, verbose_name="Mavzu")
    difficulty = models.CharField(
        max_length=20,
        choices=[("easy", "Oson"), ("medium", "O'rta"), ("hard", "Qiyin")],
        default="easy",
        verbose_name="Qiyinlik",
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return f"{self.quiz.title} — {self.order}. savol"


class ArenaQuestion(models.Model):
    arena = models.ForeignKey(Arena, on_delete=models.CASCADE, related_name="questions")
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="arena_questions")
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["arena", "question"], name="unique_arena_question"),
            models.UniqueConstraint(fields=["arena", "order"], name="unique_arena_question_order"),
        ]
        verbose_name = "Arena savoli"
        verbose_name_plural = "Arena savollari"


class ArenaParticipant(models.Model):
    arena = models.ForeignKey(Arena, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="arena_participations")
    is_owner = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveSmallIntegerField(default=0)
    total_time = models.PositiveIntegerField(default=0)
    rank = models.PositiveSmallIntegerField(null=True, blank=True)
    xp_awarded = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score", "total_time", "joined_at"]
        constraints = [
            models.UniqueConstraint(fields=["arena", "user"], name="unique_arena_participant"),
        ]
        verbose_name = "Arena ishtirokchisi"
        verbose_name_plural = "Arena ishtirokchilari"


class ArenaAnswer(models.Model):
    arena = models.ForeignKey(Arena, on_delete=models.CASCADE, related_name="answers")
    participant = models.ForeignKey(ArenaParticipant, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="arena_answers")
    selected_option = models.ForeignKey("AnswerOption", on_delete=models.SET_NULL, null=True, blank=True, related_name="arena_answers")
    is_correct = models.BooleanField(default=False)
    response_time = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["answered_at", "id"]
        constraints = [
            models.UniqueConstraint(fields=["participant", "question"], name="unique_arena_answer"),
        ]
        verbose_name = "Arena javobi"
        verbose_name_plural = "Arena javoblari"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=1000, verbose_name="Variant")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Tartib")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"

    def __str__(self):
        return self.text[:80]


class QuizAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="quiz_attempts")
    guest_id = models.CharField(max_length=128, blank=True, db_index=True)
    answers = models.JSONField(default=dict, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    correct_answers = models.PositiveSmallIntegerField(default=0)
    total_questions = models.PositiveSmallIntegerField(default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]
        verbose_name = "Test urinishi"
        verbose_name_plural = "Test urinishlari"

    def __str__(self):
        return f"{self.quiz.title} — {self.score}%"


class UserGamification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gamification")
    total_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    current_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Gamification profili"
        verbose_name_plural = "Gamification profillari"
        ordering = ["-total_points", "user__username"]

    def __str__(self):
        return f"{self.user.username} — {self.total_points} XP"


class Badge(models.Model):
    code = models.SlugField(unique=True, max_length=50)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=20, default="🏅")

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badge'lar"

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="users")
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-earned_at"]
        constraints = [models.UniqueConstraint(fields=["user", "badge"], name="unique_user_badge")]


class PointTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="point_transactions")
    points = models.PositiveIntegerField()
    reason = models.CharField(max_length=100)
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.SET_NULL, null=True, blank=True, related_name="point_transactions")
    arena = models.ForeignKey(Arena, on_delete=models.SET_NULL, null=True, blank=True, related_name="point_transactions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "XP harakati"
        verbose_name_plural = "XP harakatlari"
