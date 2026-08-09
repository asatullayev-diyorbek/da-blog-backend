from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("C dasturlash tili qaysi davrda yaratilgan?", "Tarix", "easy", "C 1970-yillarda yaratilgan.", [("1960-yillarda", False), ("1970-yillarda", True), ("1990-yillarda", False), ("2000-yillarda", False)]),
    ("C tilini kim yaratgan?", "Tarix", "easy", "C tilini Dennis Ritchie yaratgan.", [("James Gosling", False), ("Bjarne Stroustrup", False), ("Dennis Ritchie", True), ("Guido van Rossum", False)]),
    ("C dasturlash tili dastlab qaysi tashkilotda yaratilgan?", "Tarix", "easy", "C Bell Labs laboratoriyasida yaratilgan.", [("Bell Labs", True), ("Microsoft Research", False), ("Google Brain", False), ("MIT Media Lab", False)]),
    ("Quyidagilardan qaysi biri C tilida keng ishlatiladigan soha hisoblanadi?", "Qo'llanish sohalari", "easy", "C operatsion tizimlar, driverlar va embedded qurilmalarda ishlatiladi.", [("Faqat grafik dizayn", False), ("Operatsion tizimlar", True), ("Faqat elektron pochta", False), ("Faqat matn terish", False)]),
    ("Linux kernelning asosiy qismlari qaysi tilda yozilgan?", "Qo'llanish sohalari", "easy", "Darsda Linux kernel C tilida yozilgani ko'rsatilgan.", [("Python", False), ("JavaScript", False), ("C", True), ("HTML", False)]),
    ("Quyidagilardan qaysi biri C tilida yaratilgan texnologiyalardan biri?", "Qo'llanish sohalari", "easy", "Git C tilida yozilgan mashhur texnologiyalardan biridir.", [("Git", True), ("Figma", False), ("PowerPoint", False), ("Photoshop", False)]),
    ("C tilining tez ishlashining asosiy sabablaridan biri nima?", "Afzalliklar", "medium", "C kodi mashina tiliga yaqin ko'rinishga tarjima qilinadi.", [("Har doim internet talab qilishi", False), ("Kompilyatsiya qilinishi", True), ("Faqat brauzerda ishlashi", False), ("Kod yozilmasligi", False)]),
    ("C tilida xotirani boshqarish bo'yicha kim ko'proq nazoratga ega?", "Afzalliklar", "medium", "C developerga xotirani qo'lda boshqarish imkonini beradi.", [("Foydalanuvchi", False), ("Developer", True), ("Monitor", False), ("Brauzer", False)]),
    ("C tilini o'rganish boshqa tillarni o'rganishga qanday yordam beradi?", "Afzalliklar", "easy", "C kompyuter ishlashi, xotira va algoritmlarni chuqurroq tushunishga yordam beradi.", [("Faqat dizaynni o'rgatadi", False), ("Boshqa tillarni tezroq tushunishga yordam beradi", True), ("Internet tezligini oshiradi", False), ("Kompyuterni avtomatik yangilaydi", False)]),
    ("C tilining portable xususiyati nimani anglatadi?", "Afzalliklar", "medium", "Portable kod boshqa platformalarda ham ishlashi mumkinligini anglatadi.", [("Faqat bitta kompyuterda ishlashi", False), ("Boshqa platformalarda ham ishlashi mumkinligi", True), ("Faqat telefonda ishlashi", False), ("Kodsiz ishlashi", False)]),
    ("C kodini mashina kodiga tarjima qiluvchi dastur nima deb ataladi?", "Compiler va GCC", "easy", "Kodni mashina tiliga compiler tarjima qiladi.", [("Editor", False), ("Compiler", True), ("Browser", False), ("Debugger", False)]),
    ("C uchun darsda tilga olingan mashhur compiler qaysi?", "Compiler va GCC", "easy", "GCC — GNU Compiler Collection.", [("GCC", True), (" npm", False), ("Django", False), ("React", False)]),
    ("GCC qisqartmasi nimani anglatadi?", "Compiler va GCC", "medium", "GCC — GNU Compiler Collection.", [("General Code Center", False), ("GNU Compiler Collection", True), ("Global C Control", False), ("Graphical Code Compiler", False)]),
    ("C dasturining bajarilish jarayonidagi to'g'ri ketma-ketlik qaysi?", "Compiler va GCC", "medium", "Avval .c kod yoziladi, compiler orqali mashina kodi olinadi, keyin dastur bajariladi.", [(".c kod → compiler → mashina kodi → bajarish", True), ("Mashina kodi → .c kod → compiler", False), ("Browser → HTML → C", False), ("Compiler → klaviatura → .c kod", False)]),
    ("`#include <stdio.h>` qatori nima uchun kerak?", "Hello World va sintaksis", "easy", "stdio.h standart kirish-chiqish kutubxonasi bo'lib, printf uchun kerak.", [("Rasm chiqarish uchun", False), ("Standart kirish-chiqish kutubxonasini ulash uchun", True), ("Dasturni o'chirish uchun", False), ("Internetga ulanish uchun", False)]),
    ("Har bir C dasturi odatda qaysi funksiyadan boshlanadi?", "Hello World va sintaksis", "easy", "C dasturining asosiy kirish nuqtasi main() funksiyasidir.", [("start()", False), ("begin()", False), ("main()", True), ("run()", False)]),
    ("C tilida ekranga matn chiqarish uchun qaysi funksiya ishlatiladi?", "Hello World va sintaksis", "easy", "printf() ekranga formatlangan matn chiqaradi.", [("print()", False), ("printf()", True), ("writeText()", False), ("display()", False)]),
    ("C tilidagi `\\n` belgisi nimani bildiradi?", "Hello World va sintaksis", "easy", "\\n yangi qatorga o'tish belgisi.", [("Bo'sh joy", False), ("Yangi qator", True), ("Izoh", False), ("Dasturni to'xtatish", False)]),
    ("C tilida operator oxirida odatda qaysi belgi qo'yiladi?", "Hello World va sintaksis", "easy", "C operatorlari nuqta-vergul bilan tugaydi.", [("Nuqta (.)", False), ("Vergul (,)", False), ("Nuqta-vergul (;)", True), ("Ikki nuqta (:)", False)]),
    ("`return 0;` odatda nimani bildiradi?", "Hello World va sintaksis", "easy", "0 dastur muvaffaqiyatli tugaganini bildiradi.", [("Dastur xato bilan tugadi", False), ("Dastur muvaffaqiyatli tugadi", True), ("0 chiqarildi", False), ("Kompilyator yopildi", False)]),
]


class Command(BaseCommand):
    help = "C kursining 1-darsi uchun 20 ta testni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="c-dasturlash-tili").first()
        lesson = Lesson.objects.filter(course=course, order=1).first() if course else None
        if not course or not lesson:
            raise CommandError("C kursi yoki 1-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="c-1-dars-kirish-20-test",
            defaults={
                "title": "C 1-dars: C dasturlash tiliga kirish — 20 ta test",
                "description": "C tili tarixi, afzalliklari, compiler, GCC va Hello World bo'yicha test.",
                "lesson": lesson,
                "course": course,
                "category": "Dasturlash",
                "topic": "C dasturlash tiliga kirish",
                "time_limit": 600,
                "pass_score": 60,
                "randomize_questions": True,
                "published": True,
            },
        )
        quiz.questions.all().delete()
        for order, (text, topic, difficulty, explanation, options) in enumerate(QUESTIONS, 1):
            question = Question.objects.create(
                quiz=quiz,
                text=text,
                topic=topic,
                difficulty=difficulty,
                explanation=explanation,
                order=order,
            )
            AnswerOption.objects.bulk_create([
                AnswerOption(question=question, text=option_text, is_correct=is_correct, order=index)
                for index, (option_text, is_correct) in enumerate(options, 1)
            ])
        self.stdout.write(self.style.SUCCESS(f"'{quiz.title}' yaratildi: {len(QUESTIONS)} ta savol."))
