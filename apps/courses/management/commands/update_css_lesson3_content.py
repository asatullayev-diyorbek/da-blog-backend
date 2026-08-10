from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson


class Command(BaseCommand):
    help = "CSS for Beginner kursining 3-darsini yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="css-for-beginner").first()
        if not course:
            raise CommandError("CSS for Beginner kursi topilmadi.")

        content_path = Path(__file__).resolve().parents[2] / "content" / "css_lesson3.md"
        if not content_path.exists():
            raise CommandError(f"Kontent fayli topilmadi: {content_path}")

        lesson, created = Lesson.objects.get_or_create(
            course=course,
            order=3,
            defaults={
                "title": "3-Dars: Shriftlar va matn dizayni",
                "slug": "3-dars-shriftlar-va-matn-dizayni",
                "duration": "90 daqiqa",
                "is_free": True,
            },
        )
        lesson.title = "3-Dars: Shriftlar va matn dizayni"
        lesson.slug = "3-dars-shriftlar-va-matn-dizayni"
        lesson.duration = "90 daqiqa"
        lesson.is_free = True
        lesson.content = content_path.read_text(encoding="utf-8")
        lesson.save(update_fields=["title", "slug", "duration", "is_free", "content"])

        action = "yaratildi" if created else "yangilandi"
        self.stdout.write(self.style.SUCCESS(f"CSS 3-darsi {action}."))
