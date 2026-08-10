from django.core.management.base import BaseCommand

from apps.courses.models import Course


COVERS = {
    "python-beginner": "courses/covers/python-beginner-course-cover.png",
    "prompt-engineering": "courses/covers/prompt-engineering-course-cover.png",
    "sanoq-sistemalari": "courses/covers/number-systems-course-cover.png",
    "c-dasturlash-tili": "courses/covers/c-programming-course-cover.png",
}


class Command(BaseCommand):
    help = "Python, Prompt Engineering, Sanoq sistemalari va C kurslari coverlarini yangilaydi."

    def handle(self, *args, **options):
        for slug, cover in COVERS.items():
            updated = Course.objects.filter(slug=slug).update(cover=cover)
            if updated:
                self.stdout.write(self.style.SUCCESS(f"{slug}: cover yangilandi"))
            else:
                self.stdout.write(self.style.WARNING(f"{slug}: kurs topilmadi"))
