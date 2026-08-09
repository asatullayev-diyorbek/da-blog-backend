from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import AnswerOption, Question, Quiz


QUESTIONS = [
    ("Sanoq sistemasi nima?", "Asosiy tushunchalar", "easy", "Sanoq sistemasi sonlarni yozish va ifodalash qoidalaridir.", [("Sonlarni ifodalash qoidalari", True), ("Faqat amallar jadvali", False), ("Kompyuter xotirasi turi", False), ("Matn formatlash usuli", False)]),
    ("Sanoq sistemasining asosi nimani bildiradi?", "Asosiy tushunchalar", "easy", "Asos sonni yozishda nechta raqam ishlatilishini bildiradi.", [("Ishlatiladigan raqamlar sonini", True), ("Sonning uzunligini", False), ("Sonning rangini", False), ("Amallar tezligini", False)]),
    ("O'nlik sanoq sistemasining asosi nechaga teng?", "O'nlik sistema", "easy", "O'nlik sistema 10 ta raqamdan foydalanadi, shuning uchun asosi 10.", [("2", False), ("8", False), ("10", True), ("16", False)]),
    ("O'nlik sanoq sistemasida qaysi raqamlar ishlatiladi?", "O'nlik sistema", "easy", "O'nlik sistemada 0 dan 9 gacha bo'lgan raqamlar ishlatiladi.", [("0 dan 7 gacha", False), ("0 dan 9 gacha", True), ("1 dan 10 gacha", False), ("Faqat 1 va 0", False)]),
    ("Ikkilik sanoq sistemasining asosi nechaga teng?", "Ikkilik sistema", "easy", "Ikkilik sistema ikki raqamdan foydalanadi va asosi 2 ga teng.", [("2", True), ("8", False), ("10", False), ("16", False)]),
    ("Ikkilik sanoq sistemasida qaysi raqamlar mavjud?", "Ikkilik sistema", "easy", "Binary sistemada faqat 0 va 1 raqamlari ishlatiladi.", [("0 va 1", True), ("1 va 2", False), ("0 dan 7 gacha", False), ("0 dan 9 gacha", False)]),
    ("Ikkilik sanoq sistemasidagi 101 soni o'nlikda nechaga teng?", "Ikkilik sistema", "medium", "101₂ = 1×4 + 0×2 + 1×1 = 5₁₀.", [("3", False), ("4", False), ("5", True), ("6", False)]),
    ("Ikkilik 1101 sonining o'nlikdagi qiymati nechaga teng?", "Ikkilik sistema", "medium", "1101₂ = 8 + 4 + 0 + 1 = 13₁₀.", [("11", False), ("12", False), ("13", True), ("14", False)]),
    ("O'nlikdagi 10 soni ikkilikda qanday yoziladi?", "Sistemalar o'rtasida o'tish", "medium", "10₁₀ soni 1010₂ ko'rinishida yoziladi.", [("1001", False), ("1010", True), ("1100", False), ("1110", False)]),
    ("Ikkilikdagi 1000 soni o'nlikda nechaga teng?", "Sistemalar o'rtasida o'tish", "medium", "1000₂ = 1×2³ = 8₁₀.", [("4", False), ("6", False), ("8", True), ("10", False)]),
    ("Sakkizlik sanoq sistemasining asosi nechaga teng?", "Sakkizlik sistema", "easy", "Sakkizlik sistema 8 ta raqamdan foydalanadi.", [("2", False), ("8", True), ("10", False), ("16", False)]),
    ("Sakkizlik sanoq sistemasida qaysi raqam ishlatilmaydi?", "Sakkizlik sistema", "easy", "Sakkizlik sistemadagi eng katta raqam 7, shuning uchun 8 ishlatilmaydi.", [("0", False), ("5", False), ("7", False), ("8", True)]),
    ("O'n oltilik sanoq sistemasining asosi nechaga teng?", "O'n oltilik sistema", "easy", "O'n oltilik sistema 16 ta qiymatdan foydalanadi.", [("8", False), ("10", False), ("12", False), ("16", True)]),
    ("O'n oltilik sistemada A harfi qaysi qiymatni bildiradi?", "O'n oltilik sistema", "easy", "Hexadecimal sistemada A harfi 10 qiymatiga teng.", [("8", False), ("9", False), ("10", True), ("11", False)]),
    ("O'n oltilik sistemada F harfi qaysi qiymatni bildiradi?", "O'n oltilik sistema", "easy", "Hexadecimal sistemada F harfi 15 qiymatiga teng.", [("12", False), ("13", False), ("14", False), ("15", True)]),
    ("O'n oltilikdagi 2F soni o'nlikda nechaga teng?", "Sistemalar o'rtasida o'tish", "hard", "2F₁₆ = 2×16 + 15 = 47₁₀.", [("31", False), ("47", True), ("42", False), ("51", False)]),
    ("Ikkilik sonning o'ng tomondagi birinchi raqami qaysi darajaga ega?", "Razryad va darajalar", "medium", "O'ng tomondagi birinchi razryad 2⁰ qiymatiga ega.", [("2⁰", True), ("2¹", False), ("2²", False), ("10⁰", False)]),
    ("Ikkilik 1111 sonining o'nlikdagi qiymati nechaga teng?", "Sistemalar o'rtasida o'tish", "medium", "1111₂ = 8 + 4 + 2 + 1 = 15₁₀.", [("12", False), ("13", False), ("14", False), ("15", True)]),
    ("Bir xil qiymatni turli sanoq sistemalarida yozish nimani anglatadi?", "Asosiy tushunchalar", "medium", "Yozilish shakli o'zgaradi, ammo sonning qiymati bir xil qoladi.", [("Qiymat o'zgaradi", False), ("Faqat raqamlar soni o'zgaradi", False), ("Bir qiymat turlicha yozilishi mumkin", True), ("Son yo'qoladi", False)]),
    ("Uchlik sanoq sistemasida qaysi raqamlar ishlatiladi?", "Boshqa sanoq sistemalari", "easy", "Asosi 3 bo'lgan sistemada 0, 1 va 2 raqamlari ishlatiladi.", [("0, 1, 2", True), ("0, 1, 2, 3", False), ("1, 2, 3", False), ("0 va 3", False)]),
]


class Command(BaseCommand):
    help = "Sanoq sistemalari kursining 1-darsi uchun 20 ta testni yaratadi yoki yangilaydi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="sanoq-sistemalari").first()
        lesson = Lesson.objects.filter(course=course, order=1).first() if course else None
        if not course or not lesson:
            raise CommandError("Sanoq sistemalari kursi yoki 1-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="sanoq-sistemalari-1-dars-kirish-20-test",
            defaults={
                "title": "Sanoq sistemalari 1-dars: Kirish — 20 ta test",
                "description": "Sanoq sistemasi, asos, binary, octal, hexadecimal va razryadlar bo'yicha test.",
                "lesson": lesson,
                "course": course,
                "category": "Sanoq sistemalari",
                "topic": "Sanoq sistemalariga kirish",
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
