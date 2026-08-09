from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("HTML da tartibsiz ro'yxat yaratish uchun qaysi teg ishlatiladi?", "ul ro'yxati", "easy", "ul unordered list, ya'ni tartibsiz ro'yxatni bildiradi.", [("<ol>", False), ("<ul>", True), ("<list>", False), ("<items>", False)]),
    ("ul tegidagi har bir ro'yxat elementi qaysi teg bilan yoziladi?", "ul va li", "easy", "li list item, ya'ni ro'yxat elementi degani.", [("<item>", False), ("<li>", True), ("<element>", False), ("<row>", False)]),
    ("ul ro'yxatida elementlar oldida odatda nima ko'rinadi?", "ul ro'yxati", "easy", "Tartibsiz ro'yxatda raqam o'rniga nuqta yoki marker ko'rinadi.", [("Avtomatik raqam", False), ("Nuqta yoki marker", True), ("Faqat harf", False), ("Hech narsa", False)]),
    ("ul qachon ishlatiladi?", "ul ro'yxati", "easy", "Elementlar ketma-ketligi muhim bo'lmaganda ul ishlatiladi.", [("Qadamlar tartibi muhim bo'lganda", False), ("Tartib muhim bo'lmaganda", True), ("Faqat sarlavhalar uchun", False), ("Faqat rasmlar uchun", False)]),
    ("HTML da tartiblangan ro'yxat yaratish uchun qaysi teg ishlatiladi?", "ol ro'yxati", "easy", "ol ordered list, ya'ni tartiblangan ro'yxatni bildiradi.", [("<ul>", False), ("<ol>", True), ("<order>", False), ("<number>", False)]),
    ("ol ro'yxatida elementlar oldida odatda nima avtomatik chiqadi?", "ol ro'yxati", "easy", "ol ro'yxat elementlarini raqamlar bilan tartiblaydi.", [("Nuqtalar", False), ("Raqamlar", True), ("Rasmlar", False), ("Faqat chiziqlar", False)]),
    ("Qadamlar ko'rsatmasi uchun qaysi ro'yxat mos?", "ul va ol tanlovi", "easy", "Qadamlarning tartibi muhim bo'lgani uchun ol ishlatiladi.", [("ul", False), ("ol", True), ("Faqat div", False), ("Faqat span", False)]),
    ("Ingredientlar ro'yxati uchun odatda qaysi ro'yxat ishlatiladi?", "ul va ol tanlovi", "easy", "Ingredientlarning ketma-ketligi odatda muhim emas, shuning uchun ul mos.", [("ul", True), ("ol", False), ("title", False), ("table", False)]),
    ("ol type=\"A\" qanday markerlardan foydalanadi?", "ol atributlari", "easy", "A turi katta lotin harflarini beradi: A, B, C.", [("1, 2, 3", False), ("A, B, C", True), ("I, II, III", False), ("a, b, c", False)]),
    ("ol type=\"a\" qanday natija beradi?", "ol atributlari", "easy", "Kichik harfli tartib a, b, c ko'rinishida bo'ladi.", [("A, B, C", False), ("a, b, c", True), ("1, 2, 3", False), ("I, II, III", False)]),
    ("ol type=\"I\" nimani bildiradi?", "ol atributlari", "easy", "Katta rim raqamlari I, II, III ko'rinishini beradi.", [("Kichik harflar", False), ("Katta rim raqamlari", True), ("Oddiy raqamlar", False), ("Nuqtali markerlar", False)]),
    ("<ol start=\"5\"> ro'yxati qaysi raqamdan boshlanadi?", "ol atributlari", "easy", "start atributi ro'yxatning boshlang'ich qiymatini belgilaydi.", [("1 dan", False), ("5 dan", True), ("0 dan", False), ("Harflardan", False)]),
    ("reversed atributi ol ro'yxatiga qanday ta'sir qiladi?", "ol atributlari", "medium", "reversed ro'yxatni teskari tartibda ko'rsatadi.", [("Raqamlarni yashiradi", False), ("Ro'yxatni teskari tartiblaydi", True), ("Rangini o'zgartiradi", False), ("Yangi tab ochadi", False)]),
    ("Ichma-ich ro'yxat (nested list) nima?", "ichma-ich ro'yxat", "easy", "Bir ro'yxat ichida boshqa ul yoki ol joylashsa, ichma-ich ro'yxat bo'ladi.", [("Faqat bitta li ishlatilishi", False), ("li ichida boshqa ul yoki ol joylashishi", True), ("Ro'yxatni CSS bilan yashirish", False), ("Bir nechta title yozish", False)]),
    ("Ichki ul yoki ol odatda qaysi teg ichiga joylashtiriladi?", "ichma-ich ro'yxat", "medium", "Ichki ro'yxat mantiqan ota ro'yxatning li elementi ichida bo'ladi.", [("head", False), ("li", True), ("title", False), ("img", False)]),
    ("Quyidagi kodda qaysi element ichki ro'yxat hisoblanadi: <li>Frontend<ul><li>HTML</li></ul></li>?", "ichma-ich ro'yxat", "medium", "Frontend li ichidagi ul ichki ro'yxatdir.", [("Frontend", False), ("<ul> va uning HTML elementi", True), ("Faqat tashqi li", False), ("Hech biri", False)]),
    ("Ichma-ich ul ro'yxatida brauzer ko'pincha boshqa marker turini nima uchun ko'rsatadi?", "ichma-ich ro'yxat", "medium", "Darajalarni farqlash uchun brauzer ichki ro'yxatda boshqa markerdan foydalanishi mumkin.", [("Rangni majburan o'zgartirish uchun", False), ("Ro'yxat darajalarini farqlash uchun", True), ("Havola yaratish uchun", False), ("Rasmni yuklash uchun", False)]),
    ("ul ichida ol ishlatish mumkinmi?", "aralash ro'yxatlar", "easy", "HTML da ul va ol ni bir-birining ichida mantiqan ishlatish mumkin.", [("Yo'q, faqat ul bo'lishi kerak", False), ("Ha, mumkin", True), ("Faqat CSS bilan mumkin", False), ("Faqat head ichida mumkin", False)]),
    ("Retseptda asosiy qadamlar ol, har bir qadam ingredientlari ul bo'lsa, bu qanday tuzilma?", "aralash ro'yxatlar", "medium", "Asosiy tartibli qadamlar ichida tartibsiz ingredientlar joylashgan.", [("Faqat bitta ul", False), ("ol ichidagi ichma-ich ul", True), ("ul ichidagi rasm", False), ("Jadval", False)]),
    ("Navigatsiya menyusini HTML da yaratish uchun ko'p ishlatiladigan kombinatsiya qaysi?", "navigatsiya menyusi", "easy", "Menyu odatda nav, ul, li va a elementlari kombinatsiyasi bilan tuziladi.", [("nav + ul + li + a", True), ("img + table + p", False), ("head + title + meta", False), ("form + input + video", False)]),
    ("Navigatsiya menyusidagi har bir sahifa havolasi qaysi teg bilan yaratiladi?", "navigatsiya menyusi", "easy", "a tegi href orqali sahifaga o'tuvchi havolani beradi.", [("<link>", False), ("<a>", True), ("<navitem>", False), ("<go>", False)]),
    ("<nav> tegining vazifasi nima?", "navigatsiya menyusi", "easy", "nav navigatsiya havolalari joylashgan bo'limni ifodalaydi.", [("Rasmni ko'rsatish", False), ("Navigatsiya bo'limini belgilash", True), ("Video ijro etish", False), ("Jadval qatorini yaratish", False)]),
    ("Quyidagi koddagi xatoni toping: <ul><li>Bosh sahifa</ul></li>", "HTML ro'yxat tuzilmasi", "medium", "Teglar ichma-ich ochilgan tartibda yopilishi kerak: li avval, ul keyin yopiladi.", [("ul ochilmagan", False), ("li va ul yopilish tartibi noto'g'ri", True), ("ul ishlatib bo'lmaydi", False), ("Matn bo'lishi mumkin emas", False)]),
    ("Ro'yxatda har bir elementni ifodalash uchun li tegi qayerda ishlatiladi?", "HTML ro'yxat tuzilmasi", "easy", "li odatda ul yoki ol ichida ishlatiladi.", [("Faqat head ichida", False), ("ul yoki ol ichida", True), ("Faqat title ichida", False), ("Faqat img ichida", False)]),
    ("Quyidagi kod natijasi qanday bo'ladi? <ol><li>Birinchi</li><li>Ikkinchi</li></ol>", "amaliy qo'llash", "easy", "ol ichidagi ikki li element tartiblangan raqamli ro'yxat sifatida ko'rinadi.", [("Ikki nuqtali ro'yxat", False), ("1 va 2 raqamli ro'yxat", True), ("Faqat bitta sarlavha", False), ("Hech narsa", False)]),
    ("Katta rim raqamlarida uchta kurs modulini chiqarish uchun qaysi kod mos?", "amaliy qo'llash", "medium", "ol type=I ro'yxatni I, II, III ko'rinishida chiqaradi.", [("<ul type=\"I\">", False), ("<ol type=\"I\">", True), ("<ol marker=\"roman\">", False), ("<list roman=\"true\">", False)]),
]


class Command(BaseCommand):
    help = "HTML kursining 4-darsi uchun testlarni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="html-for-beginner").first()
        lesson = Lesson.objects.filter(course=course, order=4).first() if course else None
        if not course or not lesson:
            raise CommandError("HTML kursi yoki 4-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="html-4-dars-royxatlar-26-test",
            defaults={
                "title": "HTML 4-dars: Ro'yxatlar — 26 ta test",
                "description": "ul, ol, li, ol atributlari, ichma-ich ro'yxatlar va navigatsiya menyusi.",
                "lesson": lesson,
                "course": course,
                "category": "Web dasturlash",
                "topic": "HTML ro'yxatlar",
                "time_limit": 750,
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
