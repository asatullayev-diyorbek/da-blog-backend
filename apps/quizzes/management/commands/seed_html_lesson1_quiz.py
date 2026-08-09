from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("Client-server arxitekturasida client nima?", "Client va server", "easy", "Client serverdan ma'lumot so'rovchi tomon: brauzer ishlayotgan kompyuter, telefon yoki planshet.", [("Ma'lumot saqlovchi maxsus kompyuter", False), ("Serverdan ma'lumot so'rovchi tomon", True), ("Faqat internet kabeli", False), ("Web sahifa dizayni", False)]),
    ("Serverning asosiy vazifasi qaysi?", "Client va server", "easy", "Server clientlarning so'rovlarini kutadi, ma'lumotni saqlaydi va javob qaytaradi.", [("Faqat rasm chizish", False), ("So'rovlarni qabul qilib, ma'lumot va javob yuborish", True), ("Brauzerni o'rnatish", False), ("Klaviaturani boshqarish", False)]),
    ("Client serverga yuboradigan xabar nima deyiladi?", "Request va response", "easy", "Request — clientning serverga yuboradigan so'rovi.", [("Response", False), ("Request", True), ("Cookie", False), ("HTML", False)]),
    ("Serverning clientga qaytaradigan javobi nima deyiladi?", "Request va response", "easy", "Response — server requestni qayta ishlab clientga qaytaradigan javob.", [("Request", False), ("Response", True), ("Method", False), ("Domain", False)]),
    ("HTTP nimani anglatadi?", "HTTP va HTTPS", "medium", "HTTP — HyperText Transfer Protocol, ma'lumot almashish qoidalari to'plami.", [("HyperText Transfer Protocol", True), ("High Text Program", False), ("Hyperlink Transfer Page", False), ("Host Text Processing", False)]),
    ("HTTPS ning HTTP dan asosiy farqi nima?", "HTTP va HTTPS", "easy", "HTTPS ma'lumotlarni shifrlangan holda uzatadi; S — Secure.", [("Faqat rasmlar bilan ishlaydi", False), ("Ma'lumotlarni xavfsiz, shifrlangan uzatadi", True), ("Internet kerak emas", False), ("Faqat mobil qurilmada ishlaydi", False)]),
    ("200 HTTP status kodi nimani bildiradi?", "HTTP status kodlari", "easy", "200 — OK, so'rov muvaffaqiyatli bajarilgan.", [("Sahifa topilmadi", False), ("Muvaffaqiyatli bajarildi", True), ("Server xatosi", False), ("Kirish taqiqlangan", False)]),
    ("404 status kodi nimani bildiradi?", "HTTP status kodlari", "easy", "404 — Not Found, so'ralgan resurs topilmadi.", [("Muvaffaqiyatli javob", False), ("Resurs topilmadi", True), ("Yangi resurs yaratildi", False), ("Server qayta ishga tushdi", False)]),
    ("500 status kodi nimani bildiradi?", "HTTP status kodlari", "easy", "500 — Server Error, server tomonida xatolik yuz bergan.", [("Server xatosi", True), ("Topilmadi", False), ("Muvaffaqiyatli", False), ("Yo'naltirish", False)]),
    ("GET metodi odatda nima uchun ishlatiladi?", "HTTP metodlari", "easy", "GET serverdan ma'lumot olish uchun ishlatiladi.", [("Ma'lumot olish", True), ("Ma'lumot o'chirish", False), ("Profilni yangilash", False), ("Serverni o'chirish", False)]),
    ("POST metodi odatda nima uchun ishlatiladi?", "HTTP metodlari", "easy", "POST ma'lumot yuborish, masalan formani jo'natish uchun ishlatiladi.", [("Ma'lumot yuborish", True), ("Sahifa nomini o'zgartirish", False), ("Faqat ma'lumot o'qish", False), ("Faylni o'chirish", False)]),
    ("DELETE metodi qanday amalni bajaradi?", "HTTP metodlari", "easy", "DELETE resurs yoki ma'lumotni o'chirish uchun ishlatiladi.", [("Ma'lumotni olish", False), ("Ma'lumotni o'chirish", True), ("Yangi sahifa chizish", False), ("Rang berish", False)]),
    ("Web sayt nima?", "Web sayt va web sahifa", "easy", "Web sayt — bitta domenga tegishli, o'zaro bog'liq web sahifalar to'plami.", [("Faqat bitta rasm", False), ("O'zaro bog'liq web sahifalar to'plami", True), ("Faqat server kompyuteri", False), ("Brauzer oynasi", False)]),
    ("Web sahifa odatda nimani anglatadi?", "Web sayt va web sahifa", "easy", "Web sahifa — brauzerda ko'rinadigan bitta sahifa va u odatda HTML faylga asoslanadi.", [("Bitta brauzer dasturi", False), ("Brauzerda ko'rinadigan bitta sahifa", True), ("Internet provayderi", False), ("Serverning elektr ta'minoti", False)]),
    ("HTML ning to'liq nomi qaysi?", "HTML asoslari", "easy", "HTML — HyperText Markup Language.", [("HyperText Markup Language", True), ("High Transfer Machine Language", False), ("Home Text Main Link", False), ("Hyper Tool Media List", False)]),
    ("HTML qanday til hisoblanadi?", "HTML asoslari", "easy", "HTML dasturlash tili emas, web sahifa tuzilmasini belgilovchi markup tildir.", [("Dasturlash tili", False), ("Belgilash tili", True), ("Ma'lumotlar bazasi tili", False), ("Operatsion tizim", False)]),
    ("HTML faylida foydalanuvchiga ko'rinadigan asosiy kontent qaysi qismda bo'ladi?", "HTML asoslari", "medium", "body qismida foydalanuvchi ko'radigan matn, rasm, havola va boshqa elementlar bo'ladi.", [("head", False), ("body", True), ("title", False), ("doctype", False)]),
    ("CSS ning asosiy vazifasi nima?", "CSS va JavaScript", "easy", "CSS web sahifaning rang, shrift, joylashuv va boshqa ko'rinishlarini boshqaradi.", [("Sahifa dizaynini boshqarish", True), ("Serverga request yuborish", False), ("Ma'lumotlar bazasini yaratish", False), ("HTML faylini o'chirish", False)]),
    ("JavaScript web sahifaga nima qo'shadi?", "CSS va JavaScript", "easy", "JavaScript sahifaga harakat va interaktivlik qo'shadi.", [("Faqat ranglar", False), ("Harakat va interaktivlik", True), ("Faqat HTML skeleti", False), ("Internet kabeli", False)]),
    ("HTML, CSS va JavaScript munosabati qaysi javobda to'g'ri berilgan?", "CSS va JavaScript", "medium", "HTML — skelet, CSS — ko'rinish, JavaScript — harakat va interaktivlik.", [("HTML — skelet, CSS — dizayn, JS — interaktivlik", True), ("HTML — server, CSS — database, JS — kabel", False), ("HTML — faqat rang, CSS — request, JS — rasm", False), ("Uchalasining vazifasi bir xil", False)]),
]


class Command(BaseCommand):
    help = "HTML kursining 1-darsi uchun 20 ta testni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="html-for-beginner").first()
        lesson = Lesson.objects.filter(course=course, order=1).first() if course else None
        if not course or not lesson:
            raise CommandError("HTML kursi yoki 1-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="html-1-dars-web-dasturlashga-kirish-20-test",
            defaults={
                "title": "HTML 1-dars: Web dasturlashga kirish — 20 ta test",
                "description": "Client-server, HTTP, web sayt, HTML, CSS va JavaScript asoslari.",
                "lesson": lesson,
                "course": course,
                "category": "Web dasturlash",
                "topic": "Web dasturlashga kirish",
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
