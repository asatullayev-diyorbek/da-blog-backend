from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson


class Command(BaseCommand):
    help = "CSS for Beginner kursining 5-darsini yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="css-for-beginner").first()
        if not course:
            raise CommandError("CSS for Beginner kursi topilmadi.")

        content_path = Path(__file__).resolve().parents[2] / "content" / "css_lesson5.md"
        if not content_path.exists():
            raise CommandError(f"Kontent fayli topilmadi: {content_path}")

        lesson, created = Lesson.objects.get_or_create(
            course=course,
            order=5,
            defaults={
                "title": "5-Dars: Selectorlar, pseudo-class va pseudo-elementlar",
                "slug": "5-dars-selectorlar-pseudo-class-va-pseudo-elementlar",
                "duration": "90 daqiqa",
                "is_free": True,
            },
        )
        lesson.title = "5-Dars: Selectorlar, pseudo-class va pseudo-elementlar"
        lesson.slug = "5-dars-selectorlar-pseudo-class-va-pseudo-elementlar"
        lesson.duration = "90 daqiqa"
        lesson.is_free = True
        lesson.content = content_path.read_text(encoding="utf-8")
        lesson.save(update_fields=["title", "slug", "duration", "is_free", "content"])

        action = "yaratildi" if created else "yangilandi"
        self.stdout.write(self.style.SUCCESS(f"CSS 5-darsi {action}."))
