from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("C tilida o'zgaruvchi nima?", "O'zgaruvchilar", "easy", "O'zgaruvchi xotirada qiymat saqlaydigan nomlangan joydir.", [("Faqat funksiya", False), ("Qiymat saqlaydigan xotira joyi", True), ("Kompilyator nomi", False), ("Izoh turi", False)]),
    ("int yosh = 20; kodida o'zgaruvchining turi qaysi?", "O'zgaruvchilar", "easy", "int butun sonlar uchun ishlatiladi.", [("yosh", False), ("int", True), ("20", False), ("=", False)]),
    ("O'zgaruvchi qiymati dastur ishlashi davomida o'zgarishi mumkinmi?", "O'zgaruvchilar", "easy", "O'zgaruvchi qiymatini keyinchalik boshqa qiymat bilan almashtirish mumkin.", [("Yo'q, hech qachon", False), ("Ha, mumkin", True), ("Faqat char da", False), ("Faqat kompilyatsiyadan oldin", False)]),
    ("Quyidagilardan qaysi biri to'g'ri identifikator?", "Identifikatorlar", "easy", "talaba_soni harflar va pastki chiziqdan to'g'ri foydalanadi.", [("1son", False), ("talaba_soni", True), ("ism familiya", False), ("narx@1", False)]),
    ("C tilida identifikator raqam bilan boshlanishi mumkinmi?", "Identifikatorlar", "easy", "Identifikator harf yoki pastki chiziq bilan boshlanishi kerak.", [("Ha", False), ("Yo'q", True), ("Faqat int uchun", False), ("Faqat Linux da", False)]),
    ("C identifikatorida qaysi belgi ishlatilishi mumkin?", "Identifikatorlar", "easy", "Harf, raqam va pastki chiziq ruxsat etiladi, raqam esa boshida kelmaydi.", [("@", False), ("_", True), ("-", False), ("#", False)]),
    ("C tilida yosh, Yosh va YOSH qanday hisoblanadi?", "Identifikatorlar", "medium", "C katta-kichik harflarni farqlaydi.", [("Bitta identifikator", False), ("Uchta turli identifikator", True), ("Faqat YOSH ishlaydi", False), ("Kompilyator barchasini birlashtiradi", False)]),
    ("Qaysi so'zni identifikator sifatida ishlatib bo'lmaydi?", "Kalit so'zlar", "easy", "int C tilining kalit so'zi bo'lib, o'zgaruvchi nomi bo'la olmaydi.", [("yosh", False), ("int", True), ("narx1", False), ("_son", False)]),
    ("int turi nimani saqlaydi?", "Ma'lumot turlari", "easy", "int manfiy va musbat butun sonlarni saqlaydi.", [("Bitta belgi", False), ("Butun son", True), ("Faqat matn", False), ("Faqat mantiqiy qiymat", False)]),
    ("float turi qaysi qiymat uchun mos?", "Ma'lumot turlari", "easy", "float o'nli kasr sonlarni saqlash uchun ishlatiladi.", [("42", False), ("19.99", True), ("'A'", False), ("\"Salom\"", False)]),
    ("double turi float dan nimasi bilan farq qiladi?", "Ma'lumot turlari", "medium", "double odatda float ga qaraganda yuqoriroq aniqlik beradi.", [("Faqat belgilarni saqlaydi", False), ("Aniqligi yuqoriroq", True), ("Faqat butun son saqlaydi", False), ("Qiymat saqlamaydi", False)]),
    ("char o'zgaruvchisi odatda nimani saqlaydi?", "Ma'lumot turlari", "easy", "char bitta belgi uchun ishlatiladi.", [("Uzun matn", False), ("Bitta belgi", True), ("Faqat kasr son", False), ("Butun massiv", False)]),
    ("char baho = 'A'; yozuvida qiymat qaysi belgilar orasida?", "Ma'lumot turlari", "easy", "char qiymati apostrof ichida yoziladi.", [("Qo'shtirnoq", False), ("Apostrof", True), ("Qavs", False), ("Kvadrat qavs", False)]),
    ("void turi nimani anglatadi?", "Ma'lumot turlari", "medium", "void hech qanday qiymat yo'qligini bildiradi va ko'pincha funksiyalarda ishlatiladi.", [("Katta son", False), ("Bo'sh qiymat", True), ("Bitta belgi", False), ("Matn", False)]),
    ("auto o'zgaruvchisi odatda qayerda ishlatiladi?", "Storage class", "medium", "Funksiya ichidagi oddiy o'zgaruvchi auto hisoblanadi.", [("Faqat boshqa faylda", False), ("Lokal o'zgaruvchi sifatida", True), ("Faqat CPU registrida", False), ("Faqat global sohada", False)]),
    ("static o'zgaruvchining muhim xususiyati nima?", "Storage class", "medium", "static funksiya chaqiruvlari orasida qiymatini saqlab qoladi.", [("Har safar yo'qoladi", False), ("Qiymatini saqlab qoladi", True), ("Faqat matn saqlaydi", False), ("Kompilyatsiya qilinmaydi", False)]),
    ("extern kalit so'zi nima uchun ishlatiladi?", "Storage class", "medium", "extern boshqa fayl yoki qismda e'lon qilingan o'zgaruvchiga murojaat qilishga yordam beradi.", [("O'zgaruvchini o'chirish", False), ("Tashqi o'zgaruvchini e'lon qilish", True), ("Kodni izohlash", False), ("Ekranga chiqarish", False)]),
    ("printf funksiyasi qaysi kutubxonada joylashgan?", "printf", "easy", "printf va scanf stdio.h kutubxonasida joylashgan.", [("stdlib.h", False), ("stdio.h", True), ("string.h", False), ("math.h", False)]),
    ("printf funksiyasining asosiy vazifasi nima?", "printf", "easy", "printf ma'lumotni ekranga chiqaradi.", [("Klaviaturadan ma'lumot olish", False), ("Ekranga ma'lumot chiqarish", True), ("Faylni o'chirish", False), ("O'zgaruvchi yaratish", False)]),
    ("int qiymatni printf orqali chiqarish uchun qaysi format belgisi ishlatiladi?", "Format belgilari", "easy", "%d int, ya'ni butun son uchun ishlatiladi.", [("%f", False), ("%d", True), ("%c", False), ("%s", False)]),
    ("float qiymatni printf orqali chiqarish uchun qaysi format mos?", "Format belgilari", "easy", "%f float qiymatlarni chiqarish uchun ishlatiladi.", [("%d", False), ("%f", True), ("%c", False), ("%lf", False)]),
    ("Bitta char belgini printf orqali chiqarish uchun qaysi format ishlatiladi?", "Format belgilari", "easy", "%c char turidagi bitta belgini chiqaradi.", [("%s", False), ("%c", True), ("%d", False), ("%f", False)]),
    ("scanf funksiyasining asosiy vazifasi nima?", "scanf", "easy", "scanf foydalanuvchidan klaviatura orqali ma'lumot oladi.", [("Ekranga chiqarish", False), ("Foydalanuvchidan ma'lumot olish", True), ("Kodni kompilyatsiya qilish", False), ("Izoh yozish", False)]),
    ("scanf(\"%d\", &son); kodida & belgisi nima uchun kerak?", "scanf va adres operatori", "medium", "& o'zgaruvchining xotira manzilini beradi, scanf qiymatni shu joyga yozadi.", [("Sonni matnga aylantirish uchun", False), ("O'zgaruvchining manzilini berish uchun", True), ("Kodni izohlash uchun", False), ("Ekran rangini o'zgartirish uchun", False)]),
    ("scanf uchun format belgisi va o'zgaruvchi turi mos kelmasa nima yuz berishi mumkin?", "Keng tarqalgan xatolar", "medium", "Format belgisi turga mos bo'lmasa noto'g'ri natija yoki xatolik yuz berishi mumkin.", [("Har doim to'g'ri ishlaydi", False), ("Noto'g'ri natija yoki xatolik yuz berishi mumkin", True), ("Faqat matn chiqadi", False), ("Kompilyator avtomatik tuzatadi", False)]),
]


class Command(BaseCommand):
    help = "C kursining 2-darsi uchun testlarni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="c-dasturlash-tili").first()
        lesson = Lesson.objects.filter(course=course, order=2).first() if course else None
        if not course or not lesson:
            raise CommandError("C kursi yoki 2-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="c-2-dars-ozgaruvchilar-va-kiritish-25-test",
            defaults={
                "title": "C 2-dars: O'zgaruvchilar va kiritish/chiqarish — 25 ta test",
                "description": "O'zgaruvchilar, identifikatorlar, ma'lumot turlari, storage class, printf va scanf.",
                "lesson": lesson,
                "course": course,
                "category": "Dasturlash",
                "topic": "C o'zgaruvchilar va kiritish/chiqarish",
                "time_limit": 750,
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
