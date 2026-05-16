from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Course, Lesson


class LessonInline(TabularInline):
    model = Lesson
    extra = 0
    fields = ["order", "title", "slug", "duration", "is_free", "video_id"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["order"]


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ["title", "category", "level", "price", "students", "featured", "published", "created_at"]
    list_filter = ["level", "price", "featured", "published", "category"]
    search_fields = ["title", "short_description"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["featured", "published"]
    inlines = [LessonInline]
    readonly_fields = ["students", "created_at", "updated_at"]

    fieldsets = [
        ("Asosiy", {"fields": ("title", "slug", "category", "instructor")}),
        ("Kontent", {"fields": ("short_description", "cover")}),
        ("Sozlamalar", {"fields": ("level", "price", "duration", "featured", "published")}),
        ("Statistika", {"fields": ("students", "created_at", "updated_at")}),
    ]


@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ["title", "course", "order", "duration", "is_free"]
    list_filter = ["is_free", "course"]
    search_fields = ["title", "course__title"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_free", "order"]
