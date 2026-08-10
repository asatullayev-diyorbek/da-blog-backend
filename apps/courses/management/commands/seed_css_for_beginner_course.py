from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.blog.models import Category
from apps.courses.models import Course, Lesson
from apps.users.models import User


class Command(BaseCommand):
    help = "CSS for Beginner kursini yaratadi va HTML 8-darsni unga ko'chiradi."

    @transaction.atomic
    def handle(self, *args, **options):
        html_course = Course.objects.filter(slug="html-for-beginner").first()
        if not html_course:
            raise CommandError("html-for-beginner kursi topilmadi.")

        instructor = User.objects.filter(username="diyorbek").first() or html_course.instructor
        if not instructor:
            raise CommandError("Kurs instruktori topilmadi.")

        category = Category.objects.filter(slug="web-dasturlash").first()
        if not category:
            category = Category.objects.filter(name__iexact="Web dasturlash").first()
        if not category:
            category = Category.objects.filter(slug="dasturlash").first()
        if not category:
            raise CommandError("Web dasturlash kategoriyasi topilmadi.")

        css_course, created = Course.objects.update_or_create(
            slug="css-for-beginner",
            defaults={
                "title": "CSS for Beginner",
                "short_description": "CSS yordamida web sahifalarga rang, joylashuv va chiroyli dizayn berishni noldan o'rganing.",
                "cover": "courses/covers/css-for-beginner-course-cover.png",
                "category": category,
                "instructor": instructor,
                "level": "Boshlang'ich",
                "price": "Bepul",
                "duration": "1 oy",
                "published": True,
                "featured": False,
            },
        )

        lesson = (
            Lesson.objects.filter(course=html_course, order=8).first()
            or Lesson.objects.filter(course=css_course, order=1).first()
        )
        if not lesson:
            raise CommandError("HTML kursidagi 8-dars topilmadi.")

        lesson.course = css_course
        lesson.order = 1
        lesson.title = "1-Dars: CSS ga Kirish — Inline, Internal, External va Selektorlar"
        lesson.slug = "1-dars-css-ga-kirish-inline-internal-external-va-selektorlar"
        lesson.save(update_fields=["course", "order", "title", "slug"])

        action = "yaratildi" if created else "yangilandi"
        self.stdout.write(
            self.style.SUCCESS(
                f"{css_course.title} kursi {action}; '{lesson.title}' CSS kursining 1-darsi bo'ldi."
            )
        )
