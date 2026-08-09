import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.models import TelegramAuthSession
from apps.users.telegram import get_avatar_file_id, telegram_api


class Command(BaseCommand):
    help = "Telegram botni polling rejimida ishga tushiradi."

    def handle(self, *args, **options):
        offset = 0
        self.stdout.write(self.style.SUCCESS("Telegram login bot ishga tushdi."))
        while True:
            try:
                updates = telegram_api("getUpdates", {"offset": offset, "timeout": 25}, timeout=35)
                for update in updates:
                    offset = update["update_id"] + 1
                    if update.get("callback_query"):
                        self.handle_callback(update["callback_query"])
                    else:
                        self.handle_update(update)
            except KeyboardInterrupt:
                self.stdout.write("Telegram bot to'xtatildi.")
                return
            except Exception as exc:
                self.stderr.write(f"Telegram bot xatosi: {exc}")
                time.sleep(3)

    def handle_update(self, update):
        message = update.get("message") or {}
        chat = message.get("chat") or {}
        text = (message.get("text") or "").strip()
        if not chat.get("id") or not text.startswith("/start"):
            return

        chat_id = chat["id"]
        username = (message.get("from") or {}).get("username", "")
        full_name = " ".join(filter(None, [
            (message.get("from") or {}).get("first_name", ""),
            (message.get("from") or {}).get("last_name", ""),
        ]))
        payload = text.split(maxsplit=1)
        token = payload[1].strip() if len(payload) > 1 else ""
        session = TelegramAuthSession.objects.filter(token=token).first()
        if not session or not session.is_valid or session.status != "pending":
            telegram_api("sendMessage", {"chat_id": chat_id, "text": "Login link eskirgan. Saytdan qayta urinib ko'ring."})
            return
        try:
            avatar_file_id = get_avatar_file_id(chat_id)
        except Exception:
            avatar_file_id = ""
        session.chat_id = chat_id
        session.username = username
        session.full_name = full_name
        session.avatar_file_id = avatar_file_id
        session.status = "confirmation"
        session.save(update_fields=["chat_id", "username", "full_name", "avatar_file_id", "status"])
        telegram_api("sendMessage", {
            "chat_id": chat_id,
            "text": "Siz ChaqimchiAI Academy'ga kirmoqchimisiz?",
            "reply_markup": {"inline_keyboard": [[
                {"text": "✅ Ha, kirish", "callback_data": f"tg_yes:{token}"},
                {"text": "❌ Yo'q", "callback_data": f"tg_no:{token}"},
            ]]},
        })

    def handle_callback(self, callback):
        data = callback.get("data", "")
        if not data.startswith(("tg_yes:", "tg_no:")):
            return
        action, token = data.split(":", 1)
        session = TelegramAuthSession.objects.filter(token=token).first()
        callback_chat_id = (callback.get("from") or {}).get("id")
        if not session or not session.is_valid or session.status != "confirmation" or session.chat_id != callback_chat_id:
            telegram_api("answerCallbackQuery", {"callback_query_id": callback["id"], "text": "Login sessiyasi eskirgan."})
            return

        if action == "tg_yes":
            session.status = "confirmed"
            session.confirmed_at = timezone.now()
            session.save(update_fields=["status", "confirmed_at"])
            text = "✅ ChaqimchiAI Academy'ga kirildi. Saytga qaytishingiz mumkin."
        else:
            session.status = "rejected"
            session.save(update_fields=["status"])
            text = "❌ ChaqimchiAI Academy'ga kirish rad etildi."
        telegram_api("answerCallbackQuery", {"callback_query_id": callback["id"], "text": text})
        message = callback.get("message") or {}
        telegram_api("editMessageText", {
            "chat_id": callback_chat_id,
            "message_id": message.get("message_id"),
            "text": text,
            "reply_markup": {"inline_keyboard": []},
        })
