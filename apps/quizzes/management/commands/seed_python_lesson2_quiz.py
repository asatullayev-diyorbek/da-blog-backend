from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("Python da o'zgaruvchi nima?", "O'zgaruvchilar", "easy", "O'zgaruvchi qiymatni saqlash uchun ishlatiladigan nomlangan xotira joyidir.", [("Faqat funksiya", False), ("Qiymat saqlaydigan nom", True), ("HTML tegi", False), ("Faqat izoh", False)]),
    ("Python da o'zgaruvchiga qiymat berish uchun qaysi operator ishlatiladi?", "O'zgaruvchilar", "easy", "= operatori o'zgaruvchiga qiymat biriktiradi.", [("==", False), ("=", True), ("=>", False), (":=:", False)]),
    ("x = 10 kodidan keyin x ning qiymati nima bo'ladi?", "O'zgaruvchilar", "easy", "x o'zgaruvchisiga 10 qiymati biriktiriladi.", [("0", False), ("10", True), ("x", False), ("None", False)]),
    ("Bir qatorda bir nechta o'zgaruvchiga qiymat berishning to'g'ri ko'rinishi qaysi?", "O'zgaruvchilar", "medium", "Python a, b = 1, 2 ko'rinishida parallel assignment ni qo'llab-quvvatlaydi.", [("a, b = 1, 2", True), ("a = b = 1, 2", False), ("a; b := 1; 2", False), ("set(a,b,1,2)", False)]),
    ("count = 5; count = 8 bajarilgandan keyin count nimaga teng?", "O'zgaruvchilar", "easy", "Keyingi biriktirish o'zgaruvchining oldingi qiymatini almashtiradi.", [("5", False), ("8", True), ("13", False), ("Xatolik", False)]),
    ("Python o'zgaruvchi nomida bo'sh joy ishlatish mumkinmi?", "O'zgaruvchi nomlash", "easy", "O'zgaruvchi nomlarida bo'sh joy o'rniga snake_case ishlatiladi.", [("Ha, istalgancha", False), ("Yo'q, bo'sh joy ishlatilmaydi", True), ("Faqat raqamdan keyin", False), ("Faqat stringlarda", False)]),
    ("O'zgaruvchi nomini yozishda qaysi belgi ko'p ishlatiladi?", "O'zgaruvchi nomlash", "easy", "Ikki yoki undan ortiq so'z uchun snake_case, ya'ni pastki chiziq ishlatiladi.", [("Bo'sh joy", False), ("Pastki chiziq _", True), ("Nuqta .", False), ("Slash /", False)]),
    ("Qaysi o'zgaruvchi nomi Python qoidalariga mos?", "O'zgaruvchi nomlash", "easy", "user_name harf va pastki chiziqdan tashkil topgan to'g'ri nomdir.", [("2name", False), ("user-name", False), ("user_name", True), ("class", False)]),
    ("O'zgaruvchi nomini raqam bilan boshlash mumkinmi?", "O'zgaruvchi nomlash", "easy", "Python da identifikator raqam bilan boshlanmaydi.", [("Ha", False), ("Yo'q", True), ("Faqat 0 bilan", False), ("Faqat float uchun", False)]),
    ("type(25) funksiyasi nima qaytaradi?", "Ma'lumot turlari", "easy", "25 butun son bo'lgani uchun type() int turini ko'rsatadi.", [("str", False), ("int", True), ("float", False), ("bool", False)]),
    ("type(3.14) natijasi qaysi tur bo'ladi?", "Ma'lumot turlari", "easy", "O'nli sonlar float turiga kiradi.", [("int", False), ("float", True), ("str", False), ("number", False)]),
    ("type(\"25\") natijasi nima bo'ladi?", "Ma'lumot turlari", "easy", "Qo'shtirnoq ichidagi 25 son emas, matn hisoblanadi.", [("int", False), ("float", False), ("str", True), ("bool", False)]),
    ("Quyidagilardan qaysi biri list qiymatiga misol?", "Kolleksiya turlari", "easy", "List kvadrat qavslar ichida bir nechta qiymatni saqlaydi.", [("(1, 2, 3)", False), ("[1, 2, 3]", True), ("{1: 2}", False), ("<1, 2, 3>", False)]),
    ("Python da lug'at (dictionary) odatda qaysi qavs bilan yoziladi?", "Kolleksiya turlari", "easy", "Dictionary qiymatlarni kalit-qiymat juftligi sifatida jingalak qavslarda saqlaydi.", [("()", False), ("[]", False), ("{}", True), ("<>", False)]),
    ("None qiymati nimani bildiradi?", "Maxsus qiymatlar", "medium", "None qiymat yo'qligi yoki hali belgilanmaganini bildiradi.", [("0 sonini", False), ("Qiymat mavjud emasligini", True), ("False bilan bir xil har doim", False), ("Bo'sh listni", False)]),
    ("bool(0) natijasi nima?", "Boolean turi", "medium", "0 boolean kontekstda False sifatida baholanadi.", [("True", False), ("False", True), ("0", False), ("None", False)]),
    ("bool(\"\") natijasi nima?", "Boolean turi", "medium", "Bo'sh satr boolean kontekstda False hisoblanadi.", [("True", False), ("False", True), ("\"\"", False), ("Xatolik", False)]),
    ("int(\"42\") nima qiladi?", "Tur almashtirish", "easy", "int() raqam ko'rinishidagi satrni butun songa aylantiradi.", [("42 ni stringga aylantiradi", False), ("\"42\" ni 42 butun soniga aylantiradi", True), ("42 ni o'chiradi", False), ("Har doim float qaytaradi", False)]),
    ("str(100) natijasi qaysi bo'ladi?", "Tur almashtirish", "easy", "str() qiymatni satr ko'rinishiga o'tkazadi.", [("100 soni", False), ("\"100\" satri", True), ("True", False), ("None", False)]),
    ("float(5) natijasi nima?", "Tur almashtirish", "easy", "float() butun sonni o'nli son ko'rinishiga o'tkazadi.", [("5", False), ("5.0", True), ("\"5\"", False), ("False", False)]),
]


class Command(BaseCommand):
    help = "Python kursining 2-darsi uchun testlarni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug__icontains="python").first() or Course.objects.filter(title__icontains="python").first()
        lesson = Lesson.objects.filter(course=course, order=2).first() if course else None
        if not course or not lesson:
            raise CommandError("Python kursi yoki 2-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="python-2-dars-ozgaruvchilar-va-turlar-20-test",
            defaults={
                "title": "Python 2-dars: O'zgaruvchilar va ma'lumot turlari — 20 ta test",
                "description": "O'zgaruvchilarni nomlash, int, float, str, bool, list, dictionary, None va tur almashtirish.",
                "lesson": lesson,
                "course": course,
                "category": "Dasturlash",
                "topic": "Python o'zgaruvchilari va data types",
                "time_limit": 600,
                "pass_score": 60,
                "randomize_questions": True,
                "published": True,
            },
        )
        quiz.questions.all().delete()
        for order, (text, topic, difficulty, explanation, options) in enumerate(QUESTIONS, 1):
            question = Question.objects.create(quiz=quiz, text=text, topic=topic, difficulty=difficulty, explanation=explanation, order=order)
            AnswerOption.objects.bulk_create([
                AnswerOption(question=question, text=option_text, is_correct=is_correct, order=index)
                for index, (option_text, is_correct) in enumerate(options, 1)
            ])
        self.stdout.write(self.style.SUCCESS(f"'{quiz.title}' yaratildi: {len(QUESTIONS)} ta savol."))
