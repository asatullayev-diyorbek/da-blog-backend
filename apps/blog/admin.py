from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ["title", "category", "author", "published", "featured", "views", "created_at"]
    list_filter = ["published", "featured", "category"]
    search_fields = ["title", "short_description"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    list_editable = ["published", "featured"]
    date_hierarchy = "created_at"
    readonly_fields = ["views", "created_at", "updated_at"]

    fieldsets = [
        ("Asosiy", {"fields": ("title", "slug", "category", "tags", "author")}),
        ("Kontent", {"fields": ("short_description", "content", "cover")}),
        ("Sozlamalar", {"fields": ("published", "featured", "read_time")}),
        ("Statistika", {"fields": ("views", "created_at", "updated_at")}),
    ]


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ["name", "post", "approved", "created_at"]
    list_filter = ["approved"]
    list_editable = ["approved"]
    search_fields = ["name", "content"]
    readonly_fields = ["created_at"]
