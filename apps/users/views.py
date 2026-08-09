import secrets

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TelegramAuthSession, TelegramLoginCode, User
from .serializers import UserSerializer
from .telegram import create_auth_session, download_avatar, issue_user_tokens, save_avatar, upsert_telegram_user
from .telegram_bot import process_update


class TelegramAuthStartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session = create_auth_session()
        from django.conf import settings
        if not settings.TELEGRAM_BOT_USERNAME:
            return Response({"detail": "TELEGRAM_BOT_USERNAME sozlanmagan."}, status=503)
        return Response({
            "token": session.token,
            "deep_link": f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={session.token}",
            "expires_at": session.expires_at,
        })


class TelegramAuthStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        session = TelegramAuthSession.objects.filter(token=token).first()
        if not session:
            return Response({"detail": "Login sessiyasi topilmadi."}, status=404)
        if not session.is_valid and session.status not in ("confirmed", "rejected"):
            return Response({"status": "expired"})
        if session.status != "confirmed":
            return Response({"status": session.status})

        user = session.user or upsert_telegram_user(session)
        if session.user_id != user.id:
            session.user = user
            session.save(update_fields=["user"])
        return Response({
            "status": "confirmed",
            **issue_user_tokens(user),
            "user": UserSerializer(user, context={"request": request}).data,
        })


class TelegramLoginView(APIView):
    """Exchange the one-time code received from the Telegram bot for JWT tokens."""
    permission_classes = [AllowAny]

    def post(self, request):
        code = str(request.data.get("code", "")).strip()
        if len(code) != 5 or not code.isdigit():
            return Response({"detail": "5 xonali kod kiriting."}, status=400)

        with transaction.atomic():
            login_code = TelegramLoginCode.objects.select_for_update().filter(code=code).first()
            if not login_code or not login_code.is_valid:
                return Response({"detail": "Kod noto'g'ri yoki muddati tugagan."}, status=400)

            login_code.used_at = timezone.now()
            login_code.save(update_fields=["used_at"])
            user = User.objects.filter(telegram_chat_id=login_code.chat_id).first()
            is_new_user = user is None
            if not user:
                # Avval vaqtinchalik unique username bilan yaratamiz; keyin ID ma'lum bo'lgach
                # Telegram username bo'lmagan user uchun chaqimchi_0001 formatini beramiz.
                username = login_code.username or f"tg_{login_code.chat_id}"
                user = User(username=username, telegram_chat_id=login_code.chat_id)

            full_name = login_code.full_name.strip()
            name_parts = full_name.split(maxsplit=1)
            user.telegram_chat_id = login_code.chat_id
            user.telegram_username = login_code.username
            user.telegram_full_name = full_name
            user.first_name = name_parts[0] if name_parts else ""
            user.last_name = name_parts[1] if len(name_parts) > 1 else ""
            user.set_unusable_password()
            try:
                save_avatar(user, download_avatar(login_code.avatar_file_id), login_code.chat_id)
            except Exception:
                pass
            user.save()
            if not login_code.username and (is_new_user or user.username.startswith("tg_")):
                user.username = f"chaqimchi_{user.id:04d}"
                user.save(update_fields=["username"])

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user, context={"request": request}).data,
        })


class TelegramWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        supplied_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if not settings.TELEGRAM_WEBHOOK_SECRET or not secrets.compare_digest(
            supplied_secret, settings.TELEGRAM_WEBHOOK_SECRET
        ):
            return Response({"detail": "Webhook secret noto'g'ri."}, status=403)
        try:
            process_update(request.data)
        except Exception:
            return Response({"detail": "Telegram update qayta ishlanmadi."}, status=500)
        return Response({"ok": True})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user, context={"request": request}).data)
