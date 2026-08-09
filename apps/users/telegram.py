import secrets
from datetime import timedelta

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TelegramAuthSession, TelegramLoginCode, User


def telegram_api(method, payload=None, timeout=10):
    if not settings.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN sozlanmagan.")
    response = requests.post(
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/{method}",
        json=payload or {},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(data.get("description", "Telegram API xatosi."))
    return data["result"]


def make_login_code(chat_id, username="", full_name="", avatar_file_id=""):
    for _ in range(20):
        code = f"{secrets.randbelow(100000):05d}"
        if not TelegramLoginCode.objects.filter(code=code, used_at__isnull=True, expires_at__gt=timezone.now()).exists():
            return TelegramLoginCode.objects.create(
                code=code,
                chat_id=chat_id,
                username=username,
                full_name=full_name,
                avatar_file_id=avatar_file_id,
                expires_at=timezone.now() + timedelta(minutes=5),
            )
    raise RuntimeError("Login kodi yaratilmadi, qayta urinib ko'ring.")


def get_avatar_file_id(chat_id):
    photos = telegram_api("getUserProfilePhotos", {"user_id": chat_id, "limit": 1})
    if not photos.get("photos"):
        return ""
    return photos["photos"][0][-1]["file_id"]


def download_avatar(file_id):
    if not file_id:
        return None
    file_info = telegram_api("getFile", {"file_id": file_id})
    response = requests.get(
        f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_info['file_path']}",
        timeout=10,
    )
    response.raise_for_status()
    return response.content


def send_login_code(code):
    return f"Saytga kirish kodingiz: {code}\n\nKod 5 daqiqa amal qiladi. Uni hech kimga bermang."


def save_avatar(user, avatar_bytes, chat_id):
    if avatar_bytes:
        user.avatar.save(f"telegram-{chat_id}.jpg", ContentFile(avatar_bytes), save=False)


def create_auth_session():
    return TelegramAuthSession.objects.create(
        token=secrets.token_urlsafe(32),
        expires_at=timezone.now() + timedelta(minutes=5),
    )


def upsert_telegram_user(session):
    user = session.user or User.objects.filter(telegram_chat_id=session.chat_id).first()
    is_new_user = user is None
    if not user:
        user = User(username=session.username or f"tg_{session.chat_id}", telegram_chat_id=session.chat_id)

    full_name = session.full_name.strip()
    name_parts = full_name.split(maxsplit=1)
    user.telegram_chat_id = session.chat_id
    user.telegram_username = session.username
    user.telegram_full_name = full_name
    user.first_name = name_parts[0] if name_parts else ""
    user.last_name = name_parts[1] if len(name_parts) > 1 else ""
    user.set_unusable_password()
    try:
        save_avatar(user, download_avatar(session.avatar_file_id), session.chat_id)
    except Exception:
        pass
    user.save()
    if not session.username and (is_new_user or user.username.startswith("tg_")):
        user.username = f"chaqimchi_{user.id:04d}"
        user.save(update_fields=["username"])
    return user


def issue_user_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}
