from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("Python qanday turdagi dasturlash tili hisoblanadi?", "Python asoslari", "easy", "Python yuqori darajali va umumiy maqsadli dasturlash tilidir.", [("Faqat markup tili", False), ("Yuqori darajali dasturlash tili", True), ("Faqat ma'lumotlar bazasi tili", False), ("Operatsion tizim", False)]),
    ("Python dastur fayllarining kengaytmasi qaysi?", "Python asoslari", "easy", "Python kodlari odatda .py kengaytmali fayllarda saqlanadi.", [(".html", False), (".py", True), (".css", False), (".pythonfile", False)]),
    ("Python kodini ekranga chiqarish uchun qaysi funksiya ishlatiladi?", "print funksiyasi", "easy", "print() berilgan qiymatni konsolga chiqaradi.", [("show()", False), ("print()", True), ("writeScreen()", False), ("displayText()", False)]),
    ("print(\"Salom\") kodi nima qiladi?", "print funksiyasi", "easy", "Kod Salom matnini konsolga chiqaradi.", [("Salom o'zgaruvchisini o'chiradi", False), ("Salom matnini ekranga chiqaradi", True), ("Yangi fayl yaratadi", False), ("Dasturni to'xtatadi", False)]),
    ("Python da o'zgaruvchi yaratish uchun qaysi yozuv to'g'ri?", "O'zgaruvchilar", "easy", "Python da o'zgaruvchiga qiymat = operatori orqali beriladi.", [("let age = 12", False), ("age = 12", True), ("int age := 12", False), ("var age == 12", False)]),
    ("Python da o'zgaruvchi nomi katta-kichik harflarga sezgirmi?", "O'zgaruvchilar", "easy", "name va Name Python da ikki xil nom hisoblanadi.", [("Yo'q, farqi yo'q", False), ("Ha, katta-kichik harflar farqlanadi", True), ("Faqat raqamlar farqlanadi", False), ("Faqat Windows da sezgir", False)]),
    ("Quyidagi o'zgaruvchining qiymati qaysi turga tegishli: age = 14?", "Ma'lumot turlari", "easy", "Butun sonlar Python da int turiga kiradi.", [("str", False), ("int", True), ("float", False), ("bool", False)]),
    ("price = 12.5 qiymatining ma'lumot turi qaysi?", "Ma'lumot turlari", "easy", "O'nli sonlar Python da float turiga kiradi.", [("int", False), ("float", True), ("str", False), ("list", False)]),
    ("name = \"Ali\" qiymatining ma'lumot turi qaysi?", "Ma'lumot turlari", "easy", "Qo'shtirnoq ichidagi qiymat matn, ya'ni str turidir.", [("int", False), ("bool", False), ("str", True), ("float", False)]),
    ("Python da matn qiymati qanday yoziladi?", "Satrlar", "easy", "Matn qo'shtirnoq yoki bir tirnoq ichida yoziladi.", [("name = Ali", False), ("name = \"Ali\"", True), ("name == Ali", False), ("text(Ali)", False)]),
    ("True va False qiymatlari qaysi ma'lumot turiga kiradi?", "Ma'lumot turlari", "easy", "True va False mantiqiy qiymatlar bo'lib, bool turiga kiradi.", [("str", False), ("bool", True), ("int", False), ("tuple", False)]),
    ("Python da izoh (comment) yozish uchun qaysi belgi ishlatiladi?", "Izohlar", "easy", "# belgisidan keyingi qism Python tomonidan izoh sifatida qaraladi.", [("//", False), ("#", True), ("<!--", False), ("/*", False)]),
    ("Izohlar dastur bajarilganda nima bo'ladi?", "Izohlar", "easy", "Izohlar dasturchiga tushuntirish beradi va interpreter tomonidan bajarilmaydi.", [("Buyruq sifatida bajariladi", False), ("Bajarilmaydi, faqat tushuntirish bo'lib qoladi", True), ("Avtomatik o'chiriladi", False), ("HTML ga aylanadi", False)]),
    ("Python da kod bloklarini ajratishda asosan nima muhim?", "Indentatsiya", "medium", "Python kod bloklarini bo'sh joylar, ya'ni indentation orqali ajratadi.", [("Faqat nuqtali vergul", False), ("Indentatsiya", True), ("Faqat qavslar", False), ("HTML teglari", False)]),
    ("Quyidagi kodda print qaysi blok ichida? if age > 10: print(age)", "Indentatsiya", "medium", "if dan keyingi buyruq odatda ichkariga surilgan indentation bilan yoziladi.", [("if blokidan tashqarida", False), ("if blokining ichida", True), ("Faqat comment ichida", False), ("Hech qaysi blokda emas", False)]),
    ("Python da ikki qiymatni qo'shish uchun qaysi operator ishlatiladi?", "Operatorlar", "easy", "+ operatori sonlarni qo'shadi va satrlarni birlashtirishi mumkin.", [("&", False), ("+", True), ("**", False), ("=>", False)]),
    ("10 // 3 ifodasi natijasi nima bo'ladi?", "Operatorlar", "medium", "// butun bo'lish operatori bo'lib, 10 // 3 natijasi 3.", [("3", True), ("3.33", False), ("1", False), ("0", False)]),
    ("10 % 3 ifodasi nimani qaytaradi?", "Operatorlar", "medium", "% qoldiqni qaytaradi; 10 ni 3 ga bo'lganda qoldiq 1.", [("0", False), ("1", True), ("3", False), ("10", False)]),
    ("Python da foydalanuvchidan matn qabul qilish uchun qaysi funksiya ishlatiladi?", "input funksiyasi", "easy", "input() foydalanuvchidan qiymat kiritishni so'raydi va uni satr sifatida qaytaradi.", [("get()", False), ("input()", True), ("readText()", False), ("scan()", False)]),
    ("input() funksiyasi odatda qanday turdagi qiymat qaytaradi?", "input funksiyasi", "medium", "input() orqali olingan qiymat dastlab str, ya'ni satr bo'ladi.", [("Har doim int", False), ("str", True), ("Har doim bool", False), ("list", False)]),
]


class Command(BaseCommand):
    help = "Python kursining 1-darsi uchun testlarni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug__icontains="python").first() or Course.objects.filter(title__icontains="python").first()
        lesson = Lesson.objects.filter(course=course, order=1).first() if course else None
        if not course or not lesson:
            raise CommandError("Python kursi yoki 1-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="python-1-dars-kirish-20-test",
            defaults={
                "title": "Python 1-dars: Python asoslariga kirish — 20 ta test",
                "description": "Python tili, print, input, o'zgaruvchilar, ma'lumot turlari, operatorlar, izoh va indentatsiya.",
                "lesson": lesson,
                "course": course,
                "category": "Dasturlash",
                "topic": "Python asoslari",
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
