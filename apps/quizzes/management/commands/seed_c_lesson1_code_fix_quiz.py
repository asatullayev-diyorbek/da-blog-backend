from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import Question, Quiz


QUESTIONS = [
    {
        "text": "Standart kiritish-chiqarish kutubxonasini to'g'ri ulang.",
        "topic": "Hello World va sintaksis",
        "difficulty": "easy",
        "explanation": "printf() funksiyasidan foydalanish uchun stdio.h kutubxonasi ulanadi.",
        "code_template": '#include <____>\n\nint main() {\n    printf("Salom, C!");\n    return 0;\n}',
        "code_answers": ["stdio.h"],
    },
    {
        "text": "C dasturining asosiy funksiyasi nomini to'g'rilang.",
        "topic": "Hello World va sintaksis",
        "difficulty": "easy",
        "explanation": "C dasturining bajarilishi main() funksiyasidan boshlanadi.",
        "code_template": '#include <stdio.h>\n\nint ____() {\n    printf("Salom, C!");\n    return 0;\n}',
        "code_answers": ["main"],
    },
    {
        "text": "O'zgaruvchiga butun son qiymatini to'g'ri bering.",
        "topic": "O'zgaruvchilar",
        "difficulty": "easy",
        "explanation": "int o'zgaruvchiga butun son qiymati = operatori orqali beriladi.",
        "code_template": '#include <stdio.h>\n\nint main() {\n    int yosh = ____;\n    printf("%d", yosh);\n    return 0;\n}',
        "code_answers": ["14"],
    },
    {
        "text": "printf format belgisidagi xatoni tuzating.",
        "topic": "printf funksiyasi",
        "difficulty": "medium",
        "explanation": "%d belgisi int turidagi qiymatni chiqarish uchun ishlatiladi.",
        "code_template": '#include <stdio.h>\n\nint main() {\n    int yosh = 14;\n    printf("Yosh: %____", yosh);\n    return 0;\n}',
        "code_answers": ["d"],
    },
    {
        "text": "Matn chiqaruvchi funksiya nomini to'g'rilang.",
        "topic": "printf funksiyasi",
        "difficulty": "easy",
        "explanation": "C tilida konsolga matn chiqarish uchun printf() funksiyasi ishlatiladi.",
        "code_template": '#include <stdio.h>\n\nint main() {\n    ____("C tiliga xush kelibsiz!");\n    return 0;\n}',
        "code_answers": ["printf"],
    },
]


class Command(BaseCommand):
    help = "C kursining 1-darsi uchun 5 ta kod xatosini tuzatish testini yaratadi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="c-dasturlash-tili").first()
        lesson = Lesson.objects.filter(course=course, order=1).first() if course else None
        if not course or not lesson:
            raise CommandError("C kursi yoki 1-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="c-1-dars-kod-xatoni-tuzatish-5-test",
            defaults={
                "title": "C 1-dars: Kod xatosini tuzatish — 5 ta test",
                "description": "C dasturining boshlang'ich sintaksisi, printf, main va o'zgaruvchilar bo'yicha koddagi blankalarni to'ldiring.",
                "lesson": lesson,
                "course": course,
                "category": "Dasturlash",
                "topic": "C dasturlash tiliga kirish",
                "quiz_type": "code_fix",
                "time_limit": 300,
                "pass_score": 60,
                "randomize_questions": True,
                "published": True,
            },
        )
        quiz.questions.all().delete()
        Question.objects.bulk_create([
            Question(quiz=quiz, order=index, **question)
            for index, question in enumerate(QUESTIONS, 1)
        ])
        self.stdout.write(self.style.SUCCESS(f"'{quiz.title}' yaratildi: {len(QUESTIONS)} ta savol."))
