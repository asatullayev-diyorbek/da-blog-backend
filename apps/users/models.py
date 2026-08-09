from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    telegram_chat_id = models.BigIntegerField(unique=True, null=True, blank=True, db_index=True)
    telegram_username = models.CharField(max_length=150, blank=True)
    telegram_full_name = models.CharField(max_length=255, blank=True)

    @property
    def display_name(self):
        return self.telegram_full_name or self.get_full_name() or self.username

    def __str__(self):
        return self.display_name


class TelegramLoginCode(models.Model):
    code = models.CharField(max_length=5, unique=True)
    chat_id = models.BigIntegerField(db_index=True)
    username = models.CharField(max_length=150, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    avatar_file_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Telegram login kodi"
        verbose_name_plural = "Telegram login kodlari"

    @property
    def is_valid(self):
        return self.used_at is None and timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.code} — {self.chat_id}"


class TelegramAuthSession(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("confirmation", "Tasdiq kutilmoqda"),
        ("confirmed", "Tasdiqlangan"),
        ("rejected", "Rad etilgan"),
    ]

    token = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    chat_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    username = models.CharField(max_length=150, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    avatar_file_id = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="telegram_auth_sessions")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Telegram auth sessiyasi"
        verbose_name_plural = "Telegram auth sessiyalari"

    @property
    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.token[:8]} — {self.status}"
