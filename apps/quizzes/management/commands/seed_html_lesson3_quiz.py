from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("HTML da havola yaratish uchun qaysi teg ishlatiladi?", "a tegi va href", "easy", "a (anchor) tegi havola yaratadi.", [("<link>", False), ("<a>", True), ("<url>", False), ("<href>", False)]),
    ("a tegi nomidagi anchor so'zi nimani anglatadi?", "a tegi va href", "easy", "Anchor so'zi langar ma'nosini anglatadi.", [("Sarlavha", False), ("Langar", True), ("Rasm", False), ("Oyna", False)]),
    ("Havolaning qayerga o'tishini qaysi atribut belgilaydi?", "a tegi va href", "easy", "href atributi havolaning manzilini belgilaydi.", [("src", False), ("href", True), ("alt", False), ("target", False)]),
    ("<a href=\"https://google.com\">Google</a> kodida foydalanuvchi nimani bosadi?", "a tegi va href", "easy", "Ochiluvchi va yopiluvchi a teglari orasidagi Google matni havola ko'rinishida chiqadi.", [("https://google.com matnini", False), ("Google matnini", True), ("href atributini", False), ("a harfini", False)]),
    ("target=\"_blank\" atributi nima qiladi?", "target atributi", "easy", "_blank havolani yangi tab yoki oynada ochadi.", [("Havolani o'chiradi", False), ("Havolani yangi tabda ochadi", True), ("Rasmni kattalashtiradi", False), ("Sahifani yopadi", False)]),
    ("target=\"_self\" qanday natija beradi?", "target atributi", "easy", "_self havolani joriy tabda ochadi.", [("Yangi tab ochadi", False), ("Joriy tabda ochadi", True), ("Faqat email ochadi", False), ("Havolani yashiradi", False)]),
    ("Tashqi havolaga misolni toping.", "Havola turlari", "easy", "Boshqa domen manziliga o'tuvchi havola tashqi havola hisoblanadi.", [("href=\"kontakt.html\"", False), ("href=\"https://python.org\"", True), ("href=\"#top\"", False), ("href=\"../rasm.jpg\"", False)]),
    ("Ichki havola odatda nimaga olib boradi?", "Havola turlari", "easy", "Ichki havola o'z saytingizning boshqa HTML sahifasiga olib boradi.", [("Boshqa saytdagi domenga", False), ("O'z saytingizdagi boshqa sahifaga", True), ("Faqat email dasturiga", False), ("Faqat telefon qo'ng'irog'iga", False)]),
    ("Sahifa ichidagi ma'lum qismga o'tish uchun qaysi yozuv ishlatiladi?", "Havola turlari", "medium", "Elementga id berilib, href qiymatida uning nomiga # bilan murojaat qilinadi.", [("href=\"/id\"", False), ("href=\"#bo lim-id\"", True), ("href=\"@id\"", False), ("href=\"id:\"", False)]),
    ("Sahifa ichidagi havola ishlashi uchun manzil elementida qaysi atribut bo'lishi kerak?", "Havola turlari", "easy", "Havola olib boradigan elementga id atributi beriladi.", [("class", False), ("id", True), ("src", False), ("alt", False)]),
    ("Email havolasi qaysi protokol bilan boshlanadi?", "Email va telefon havolalari", "easy", "mailto: bosilganda email dasturini ochadigan havola yaratadi.", [("email:", False), ("mailto:", True), ("mail:", False), ("smtp:", False)]),
    ("Telefon havolasi qaysi protokol bilan yoziladi?", "Email va telefon havolalari", "easy", "tel: mobil qurilmada telefon raqamiga qo'ng'iroq qilish imkonini beradi.", [("phone:", False), ("tel:", True), ("call:", False), ("mobile:", False)]),
    ("Rasmni HTML sahifaga qo'shish uchun qaysi teg ishlatiladi?", "img tegi va atributlari", "easy", "img tegi sahifaga rasm qo'shadi.", [("<picture-src>", False), ("<img>", True), ("<image>", False), ("<photo>", False)]),
    ("img tegidagi src atributi nimani bildiradi?", "img tegi va atributlari", "easy", "src source so'zidan kelib chiqib rasm manzilini ko'rsatadi.", [("Rasm tavsifini", False), ("Rasm manzilini", True), ("Rasm rangini", False), ("Rasm nomini ekranga chiqarishni", False)]),
    ("img tegidagi alt atributi nima uchun kerak?", "img tegi va atributlari", "easy", "alt rasm yuklanmasa yoki ekran o'quvchi ishlatilsa ko'riladigan alternativ matndir.", [("Rasm o'lchamini berish uchun", False), ("Rasm ko'rinmasa chiqadigan alternativ matn uchun", True), ("Rasmga link berish uchun", False), ("Rasmni o'chirish uchun", False)]),
    ("alt atributi yana qaysi ikki yo'nalish uchun muhim?", "img tegi va atributlari", "medium", "Darsda alt SEO va accessibility uchun muhimligi ko'rsatilgan.", [("SEO va accessibility", True), ("Faqat animatsiya va video", False), ("Faqat server va database", False), ("Faqat rang va shrift", False)]),
    ("img tegi qanday element hisoblanadi?", "img tegi va atributlari", "easy", "img yopilmaydigan teg hisoblanadi.", [("Juft, yopilishi shart bo'lgan teg", False), ("Yopilmaydigan teg", True), ("Faqat CSS elementi", False), ("Faqat head ichidagi teg", False)]),
    ("Rasm kengligi va balandligini qaysi atributlar belgilaydi?", "Rasm o'lchamlari", "easy", "width kenglikni, height balandlikni belgilaydi.", [("size va scale", False), ("width va height", True), ("wide va tall", False), ("x va y", False)]),
    ("img ga faqat width berilsa odatda nima sodir bo'ladi?", "Rasm o'lchamlari", "medium", "Faqat width berilganda brauzer balandlikni proporsiyaga mos hisoblaydi.", [("Rasm avtomatik o'chadi", False), ("Balandlik avtomatik hisoblanib, proporsiya saqlanadi", True), ("Rasm doim kvadrat bo'ladi", False), ("alt yo'qoladi", False)]),
    ("width=\"50%\" nimaga nisbatan rasm kengligini belgilaydi?", "Rasm o'lchamlari", "easy", "Foiz qiymati sahifa yoki ota element kengligiga nisbatan qo'llanadi.", [("Har doim 50 piksel", False), ("Sahifa kengligiga nisbatan", True), ("Rasm balandligiga nisbatan", False), ("Brauzer tabiga nisbatan", False)]),
    ("https://example.com/rasm.jpg qanday yo'l hisoblanadi?", "Rasm manzili", "easy", "To'liq internet manzili mutlaq (absolute) yo'l hisoblanadi.", [("Nisbiy yo'l", False), ("Mutlaq yo'l", True), ("Sahifa ichidagi anchor", False), ("Email yo'li", False)]),
    ("HTML fayl bilan bir papkadagi rasm uchun qaysi src to'g'ri?", "Rasm manzili", "easy", "Bir papkadagi faylga to'g'ridan-to'g'ri fayl nomi bilan murojaat qilinadi.", [("src=\"/rasm.jpg\"", False), ("src=\"rasm.jpg\"", True), ("src=\"#rasm.jpg\"", False), ("src=\"mailto:rasm.jpg\"", False)]),
    ("images papkasidagi profil.png rasmiga qaysi yo'l to'g'ri?", "Rasm manzili", "easy", "images papkasi ichidagi faylga images/profil.png ko'rinishida murojaat qilinadi.", [("src=\"profil.png/images\"", False), ("src=\"images/profil.png\"", True), ("src=\"../images\"", False), ("src=\"#images/profil.png\"", False)]),
    ("../rasm.jpg nisbiy yo'li nimani anglatadi?", "Rasm manzili", "medium", ".. joriy papkaning bir pog'ona yuqorisini bildiradi.", [("Joriy papkadagi rasm", False), ("Bir papka yuqoridagi rasm", True), ("Internetdagi rasm", False), ("Rasmning ikkinchi nusxasi", False)]),
    ("Rasmni bosiladigan havolaga aylantirish uchun nima qilish kerak?", "Rasm-havola", "easy", "img tegini a tegining ichiga joylash rasmni bosiladigan havolaga aylantiradi.", [("a tegini img ichiga yozish", False), ("img tegini a tegi ichiga yozish", True), ("Faqat alt qo'shish", False), ("src ni href ga almashtirish", False)]),
    ("Quyidagi kod bosilganda nima bo'ladi? <a href=\"https://python.org\"><img src=\"logo.png\" alt=\"Python\"></a>", "Rasm-havola", "medium", "a ichidagi rasm bosiladigan bo'ladi va python.org manziliga olib boradi.", [("Rasm o'chadi", False), ("Rasm bosilganda python.org ochiladi", True), ("Faqat rasm nomi chiqadi", False), ("Yangi HTML fayl yaratiladi", False)]),
    ("Tashqi havolalarda target=\"_blank\" ishlatishning foydasi nima?", "Amaliy qo'llash", "medium", "Yangi tab ochilishi foydalanuvchiga joriy sahifani yo'qotmaslikka yordam beradi.", [("Joriy sahifani saqlab, tashqi sahifani yangi tabda ochadi", True), ("Rasmni avtomatik yuklaydi", False), ("Saytni tezlashtiradi", False), ("Havolani yashiradi", False)]),
]


class Command(BaseCommand):
    help = "HTML kursining 3-darsi uchun testlarni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="html-for-beginner").first()
        lesson = Lesson.objects.filter(course=course, order=3).first() if course else None
        if not course or not lesson:
            raise CommandError("HTML kursi yoki 3-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="html-3-dars-havolalar-va-rasmlar-27-test",
            defaults={
                "title": "HTML 3-dars: Havolalar va rasmlar — 27 ta test",
                "description": "a, href, target, havola turlari, img, src, alt, o'lcham va rasm yo'llari.",
                "lesson": lesson,
                "course": course,
                "category": "Web dasturlash",
                "topic": "Havolalar va rasmlar",
                "time_limit": 810,
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
