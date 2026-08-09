from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import AnswerOption, Arena, ArenaAnswer, ArenaParticipant, ArenaQuestion, Badge, PointTransaction, Question, Quiz, QuizAttempt, UserBadge, UserGamification


class AnswerOptionInline(TabularInline):
    model = AnswerOption
    extra = 2
    fields = ["order", "text", "is_correct"]


class QuestionInline(TabularInline):
    model = Question
    extra = 0
    fields = ["order", "text", "explanation"]
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(ModelAdmin):
    list_display = ["title", "course", "category", "topic", "lesson", "pass_score", "published", "created_at"]
    list_filter = ["published", "randomize_questions"]
    search_fields = ["title", "description", "category", "topic"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [QuestionInline]
    list_editable = ["published"]


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ["__str__", "quiz", "topic", "difficulty", "order"]
    list_filter = ["quiz"]
    search_fields = ["text"]
    inlines = [AnswerOptionInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(ModelAdmin):
    list_display = ["quiz", "user", "guest_id", "score", "passed", "completed_at"]
    list_filter = ["passed", "quiz"]
    search_fields = ["guest_id", "user__username", "quiz__title"]
    readonly_fields = ["id", "started_at", "completed_at"]


@admin.register(Arena)
class ArenaAdmin(ModelAdmin):
    list_display = ["code", "owner", "status", "question_count", "max_players", "created_at"]
    list_filter = ["status"]
    search_fields = ["code", "owner__username"]
    readonly_fields = ["id", "code", "created_at"]


@admin.register(ArenaParticipant)
class ArenaParticipantAdmin(ModelAdmin):
    list_display = ["arena", "user", "is_owner", "score", "correct_answers", "rank", "xp_awarded"]
    list_filter = ["is_owner", "xp_awarded"]
    search_fields = ["arena__code", "user__username"]


@admin.register(ArenaQuestion)
class ArenaQuestionAdmin(ModelAdmin):
    list_display = ["arena", "order", "question"]
    list_filter = ["arena"]


@admin.register(ArenaAnswer)
class ArenaAnswerAdmin(ModelAdmin):
    list_display = ["arena", "participant", "question", "is_correct", "points", "response_time"]
    list_filter = ["is_correct", "arena"]


@admin.register(UserGamification)
class UserGamificationAdmin(ModelAdmin):
    list_display = ["user", "total_points", "level", "current_streak", "last_activity_date"]
    search_fields = ["user__username"]
    readonly_fields = ["total_points", "level", "current_streak", "last_activity_date"]


@admin.register(Badge)
class BadgeAdmin(ModelAdmin):
    list_display = ["icon", "name", "code"]
    search_fields = ["name", "code"]


@admin.register(UserBadge)
class UserBadgeAdmin(ModelAdmin):
    list_display = ["user", "badge", "earned_at"]
    list_filter = ["badge"]
    search_fields = ["user__username", "badge__name"]
    readonly_fields = ["earned_at"]


@admin.register(PointTransaction)
class PointTransactionAdmin(ModelAdmin):
    list_display = ["user", "points", "reason", "attempt", "arena", "created_at"]
    list_filter = ["reason"]
    search_fields = ["user__username", "reason"]
    readonly_fields = ["created_at"]
