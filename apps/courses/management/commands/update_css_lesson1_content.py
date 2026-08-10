from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson


class Command(BaseCommand):
    help = "CSS for Beginner kursining 1-darsiga to'liq kontent joylaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="css-for-beginner").first()
        lesson = Lesson.objects.filter(
            course=course,
            slug="1-dars-css-ga-kirish-inline-internal-external-va-selektorlar",
        ).first() if course else None
        if not course or not lesson:
            raise CommandError("CSS kursi yoki 1-dars topilmadi.")

        content_path = Path(__file__).resolve().parents[2] / "content" / "css_lesson1.md"
        if not content_path.exists():
            raise CommandError(f"Kontent fayli topilmadi: {content_path}")

        lesson.content = content_path.read_text(encoding="utf-8")
        lesson.title = "1-Dars: CSS ga kirish — web sahifaga dizayn berish"
        lesson.duration = "90 daqiqa"
        lesson.is_free = True
        lesson.save(update_fields=["content", "title", "duration", "is_free"])
        self.stdout.write(self.style.SUCCESS("CSS 1-darsining to'liq kontenti joylandi."))
