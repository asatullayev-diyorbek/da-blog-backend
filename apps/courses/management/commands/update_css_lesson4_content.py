from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson


class Command(BaseCommand):
    help = "CSS for Beginner kursining 4-darsini yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="css-for-beginner").first()
        if not course:
            raise CommandError("CSS for Beginner kursi topilmadi.")

        content_path = Path(__file__).resolve().parents[2] / "content" / "css_lesson4.md"
        if not content_path.exists():
            raise CommandError(f"Kontent fayli topilmadi: {content_path}")

        lesson, created = Lesson.objects.get_or_create(
            course=course,
            order=4,
            defaults={
                "title": "4-Dars: CSS Box Model — o‘lcham, oraliq va chegara",
                "slug": "4-dars-css-box-model-olcham-oraliq-va-chegara",
                "duration": "90 daqiqa",
                "is_free": True,
            },
        )
        lesson.title = "4-Dars: CSS Box Model — o‘lcham, oraliq va chegara"
        lesson.slug = "4-dars-css-box-model-olcham-oraliq-va-chegara"
        lesson.duration = "90 daqiqa"
        lesson.is_free = True
        lesson.content = content_path.read_text(encoding="utf-8")
        lesson.save(update_fields=["title", "slug", "duration", "is_free", "content"])

        action = "yaratildi" if created else "yangilandi"
        self.stdout.write(self.style.SUCCESS(f"CSS 4-darsi {action}."))
