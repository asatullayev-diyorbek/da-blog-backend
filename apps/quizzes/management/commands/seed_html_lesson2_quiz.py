from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("HTML5 faylini brauzerga bildirish uchun qaysi deklaratsiya yoziladi?", "HTML fayl tuzilmasi", "easy", "DOCTYPE brauzerga hujjat HTML5 ekanini bildiradi.", [("<html5>", False), ("<!DOCTYPE html>", True), ("<meta html5>", False), ("<document html>", False)]),
    ("HTML hujjatidagi barcha asosiy kontent qaysi bosh teg ichida bo'ladi?", "HTML fayl tuzilmasi", "easy", "html tegi butun HTML hujjatining bosh elementi hisoblanadi.", [("<head>", False), ("<html>", True), ("<body>", False), ("<main>", False)]),
    ("<head> qismida odatda qanday ma'lumotlar saqlanadi?", "HTML fayl tuzilmasi", "easy", "head foydalanuvchiga ko'rinmaydigan texnik ma'lumotlarni saqlaydi.", [("Foydalanuvchi ko'radigan barcha matn", False), ("Sahifa nomi, encoding va stillar kabi texnik ma'lumotlar", True), ("Faqat rasmlar", False), ("Faqat tugmalar", False)]),
    ("UTF-8 encodingini belgilash uchun qaysi yozuv ishlatiladi?", "HTML fayl tuzilmasi", "medium", "meta charset=UTF-8 o'zbek harflari kabi belgilarni to'g'ri ko'rsatishga yordam beradi.", [("<meta charset=\"UTF-8\">", True), ("<charset utf=\"8\">", False), ("<encoding>UTF</encoding>", False), ("<meta language=\"uz\">", False)]),
    ("<title> tegi matni qayerda ko'rinadi?", "HTML fayl tuzilmasi", "easy", "title brauzer oynasining tabida ko'rinadigan sahifa nomini beradi.", [("Sahifaning pastida", False), ("Brauzer tabida", True), ("Faqat server logida", False), ("Rasm ichida", False)]),
    ("VS Code'da ! yozib Tab bosish odatda nima yaratadi?", "HTML fayl tuzilmasi", "easy", "Emmet yordamida ! + Tab HTML boshlang'ich skeletini avtomatik yaratadi.", [("CSS animatsiyasini", False), ("HTML faylining asosiy tuzilmasini", True), ("Faqat paragrafni", False), ("Serverni", False)]),
    ("Qaysi sarlavha tegi eng katta va eng muhim hisoblanadi?", "Sarlavha teglari", "easy", "h1 birinchi darajali, eng katta va asosiy sarlavha hisoblanadi.", [("<h6>", False), ("<h3>", False), ("<h1>", True), ("<heading>", False)]),
    ("h1 dan h6 gacha sarlavhalarda h6 nimani anglatadi?", "Sarlavha teglari", "easy", "h6 sarlavhalar ichida eng kichik darajadir.", [("Eng katta sarlavha", False), ("Eng kichik sarlavha", True), ("Yashirin sarlavha", False), ("Noto'g'ri teg", False)]),
    ("Professional sahifada odatda h1 nechta bo'lishi tavsiya qilinadi?", "Sarlavha teglari", "medium", "Darsda sahifaning asosiy sarlavhasi sifatida odatda bitta h1 ishlatilishi aytilgan.", [("Odatda bitta", True), ("Har bir paragraf uchun bittadan", False), ("Hech qachon bo'lmaydi", False), ("Faqat oltita", False)]),
    ("Paragraf yaratish uchun qaysi teg ishlatiladi?", "Paragraf va qator", "easy", "p paragraph so'zidan kelib chiqqan va matn blokini yaratadi.", [("<text>", False), ("<p>", True), ("<paragraph>", False), ("<line>", False)]),
    ("Har bir p tegi brauzerda odatda qanday ko'rinadi?", "Paragraf va qator", "easy", "Har bir p yangi paragraf bo'lib, brauzer ular orasiga bo'shliq qo'shadi.", [("Yangi paragraf va bo'shliq bilan", True), ("Har doim qalin matn bo'lib", False), ("Rasm sifatida", False), ("Umuman ko'rinmaydi", False)]),
    ("HTML kodidagi ko'p bo'shliqlar brauzerda qanday ko'rsatiladi?", "Paragraf va qator", "medium", "HTMLdagi ketma-ket bo'shliqlar brauzer tomonidan odatda bitta bo'shliq sifatida ko'rsatiladi.", [("Hammasi saqlanadi", False), ("Bitta bo'shliq sifatida", True), ("Avtomatik o'chadi", False), ("Tabga aylanadi", False)]),
    ("Yangi qatorga o'tish uchun qaysi teg ishlatiladi?", "br va hr", "easy", "br line break bo'lib, matnni keyingi qatorga o'tkazadi.", [("<new-line>", False), ("<br>", True), ("<breakline>", False), ("<p>", False)]),
    ("br tegi qanday teg hisoblanadi?", "br va hr", "easy", "br yopilmaydigan, ya'ni void element hisoblanadi.", [("Juft va majburiy yopiladigan", False), ("Yopilmaydigan", True), ("Faqat head ichida ishlaydigan", False), ("Faqat CSS tegi", False)]),
    ("hr tegi nima chiqaradi?", "br va hr", "easy", "hr sahifa bo'limlarini ajratuvchi gorizontal chiziq chiqaradi.", [("Vertikal rasm", False), ("Gorizontal ajratuvchi chiziq", True), ("Yangi oyna", False), ("Qalin sarlavha", False)]),
    ("Qaysi teg matnni qalin ko'rinishda chiqaradi?", "Matn formatlash", "easy", "b va strong teglarining ikkalasi ham matnni qalin ko'rsatadi.", [("<i>", False), ("<b>", True), ("<u>", False), ("<small>", False)]),
    ("Qaysi teg matnni qiyshiq ko'rinishda chiqaradi?", "Matn formatlash", "easy", "i va em teglarining ikkalasi ham qiyshiq matn ko'rinishini beradi.", [("<i>", True), ("<mark>", False), ("<del>", False), ("<sub>", False)]),
    ("Matn tagiga chizish uchun qaysi teg ishlatiladi?", "Matn formatlash", "easy", "u underline ma'nosida bo'lib, matn tagiga chiziq chizadi.", [("<underline>", False), ("<u>", True), ("<line>", False), ("<ins>", False)]),
    ("mark tegi qanday ko'rinish beradi?", "Matn formatlash", "easy", "mark matnni odatda sariq fon bilan ta'kidlab ko'rsatadi.", [("Matnni yashiradi", False), ("Matnni ta'kidlangan, sariq fonli ko'rinishda beradi", True), ("Matnni o'chiradi", False), ("Matnni indeksga aylantiradi", False)]),
    ("small tegi nima uchun ishlatiladi?", "Matn formatlash", "easy", "small matnni kichikroq ko'rinishda chiqaradi.", [("Kichik matn chiqarish", True), ("Qalin matn chiqarish", False), ("Rasmni kichraytirish", False), ("Sahifani yopish", False)]),
    ("del va ins teglari qaysi juftlikni bildiradi?", "Matn formatlash", "medium", "del o'chirilgan eski matnni, ins esa qo'shilgan yangi matnni bildiradi.", [("Rasm va video", False), ("O'chirilgan va qo'shilgan matn", True), ("Yuqori va pastki indeks", False), ("Qalin va qiyshiq matn", False)]),
    ("H2O formulasida 2 ni pastki indeks qilib ko'rsatish uchun qaysi teg kerak?", "Indekslar", "easy", "sub pastki indeks uchun ishlatiladi: H<sub>2</sub>O.", [("<sup>", False), ("<sub>", True), ("<down>", False), ("<small>", False)]),
    ("10² ko'rinishidagi yuqori indeksni qaysi teg yaratadi?", "Indekslar", "easy", "sup yuqori indeks uchun ishlatiladi: 10<sup>2</sup>.", [("<top>", False), ("<sup>", True), ("<sub>", False), ("<mark>", False)]),
    ("b va strong teglari orasidagi asosiy semantik farq nima?", "Semantik teglar", "medium", "b faqat vizual qalinlik beradi, strong esa matn muhimligini semantik bildiradi.", [("Ular mutlaqo boshqa rang beradi", False), ("strong matn muhimligini semantik bildiradi, b esa asosan vizual ko'rinish uchun", True), ("b faqat rasm uchun ishlaydi", False), ("strong yopilmaydigan teg", False)]),
    ("i va em orasidagi farq qaysi javobda to'g'ri?", "Semantik teglar", "medium", "i asosan vizual qiyshiqlik, em esa ta'kid ma'nosini beradi.", [("em semantik ta'kid beradi, i esa asosan vizual ko'rinish uchun", True), ("i faqat sarlavha uchun", False), ("em faqat rasm uchun", False), ("Ularning vazifasi mutlaqo qarama-qarshi", False)]),
    ("HTML izohi (comment) qaysi sintaksisda yoziladi?", "HTML izohlari", "easy", "HTML izohi <!-- va --> orasida yoziladi va brauzerda ko'rinmaydi.", [("// izoh", False), ("<!-- izoh -->", True), ("/* izoh */", False), ("# izoh", False)]),
    ("HTML comment brauzerda foydalanuvchiga ko'rinadimi?", "HTML izohlari", "easy", "Izoh kod ichida qoladi va brauzer sahifasida ko'rsatilmaydi.", [("Ha, doim ko'rinadi", False), ("Yo'q, ko'rinmaydi", True), ("Faqat mobil qurilmada ko'rinadi", False), ("Faqat title ichida ko'rinadi", False)]),
    ("Bir nechta qatorni vaqtincha izohga olish uchun nima qilish mumkin?", "HTML izohlari", "medium", "Bir nechta qator <!-- va --> orasiga olinadi.", [("Har bir qatorga title yozish", False), ("Barcha qatorlarni <!-- va --> orasiga olish", True), ("Faqat <p> bilan o'rash", False), ("CSS fayliga ko'chirish", False)]),
    ("Kursdagi mustaqil ishda kitob nomi qaysi tegda, muallifi qaysi tegda bo'lishi kerak?", "Amaliy qo'llash", "medium", "Kitob sahifasi mashqida nom h1, muallif h2, nashr yili h3 sifatida beriladi.", [("Nom h3, muallif h1, yil h6", False), ("Nom h1, muallif h2, yil h3", True), ("Hammasi p", False), ("Nom title, muallif meta, yil head", False)]),
]


class Command(BaseCommand):
    help = "HTML kursining 2-darsi uchun testlarni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="html-for-beginner").first()
        lesson = Lesson.objects.filter(course=course, order=2).first() if course else None
        if not course or not lesson:
            raise CommandError("HTML kursi yoki 2-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="html-2-dars-asosiy-teglar-28-test",
            defaults={
                "title": "HTML 2-dars: Asosiy teglar — 29 ta test",
                "description": "HTML fayl tuzilmasi, sarlavha, paragraf, formatlash, indeks va comment teglari.",
                "lesson": lesson,
                "course": course,
                "category": "Web dasturlash",
                "topic": "HTML asosiy teglar",
                "time_limit": 840,
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
