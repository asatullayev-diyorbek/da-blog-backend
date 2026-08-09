from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import TelegramAuthSession, TelegramLoginCode, User


@admin.register(User)
class UserAdmin(ModelAdmin, BaseUserAdmin):
    list_display = ["username", "email", "first_name", "is_staff", "date_joined"]
    list_filter = ["is_staff", "is_superuser", "is_active"]
    search_fields = ["username", "email", "first_name", "last_name"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Profil", {"fields": ("avatar", "bio", "telegram_chat_id", "telegram_username", "telegram_full_name")}),
    )


@admin.register(TelegramLoginCode)
class TelegramLoginCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "chat_id", "username", "expires_at", "used_at"]
    search_fields = ["code", "chat_id", "username", "full_name"]
    readonly_fields = ["code", "chat_id", "username", "full_name", "avatar_file_id", "created_at", "expires_at", "used_at"]


@admin.register(TelegramAuthSession)
class TelegramAuthSessionAdmin(admin.ModelAdmin):
    list_display = ["token", "status", "chat_id", "username", "user", "expires_at", "confirmed_at"]
    list_filter = ["status"]
    search_fields = ["token", "chat_id", "username", "full_name"]
    readonly_fields = ["token", "created_at", "confirmed_at"]
