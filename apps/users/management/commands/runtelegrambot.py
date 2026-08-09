import time

from django.core.management.base import BaseCommand

from apps.users.telegram import telegram_api
from apps.users.telegram_bot import process_update


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
                    process_update(update)
            except KeyboardInterrupt:
                self.stdout.write("Telegram bot to'xtatildi.")
                return
            except Exception as exc:
                self.stderr.write(f"Telegram bot xatosi: {exc}")
                time.sleep(3)
