from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course, Lesson
from apps.quizzes.models import Question, Quiz


def question(text, topic, *parts):
    # Difficulty is optional so a content typo cannot shift the code template
    # into the answer field. Existing entries without it default to easy.
    if parts and parts[0] in {"easy", "medium", "hard"}:
        difficulty, explanation, code_template, *answers = parts
    else:
        difficulty = "easy"
        explanation, code_template, *answers = parts
    return {
        "text": text,
        "topic": topic,
        "difficulty": difficulty,
        "explanation": explanation,
        "code_template": code_template,
        "code_answers": list(answers),
    }


QUESTIONS = [
    # Input / output va ma'lumot turlari: 1-10
    question("Foydalanuvchidan butun son olish uchun scanf formatini to'g'rilang.", "Input/output", "easy", "%d int qiymat uchun, & esa o'zgaruvchi manzilini beradi.", '#include <stdio.h>\nint main() {\n    int son;\n    scanf("____", &son);\n    return 0;\n}', "%d"),
    question("scanf funksiyasiga o'zgaruvchining manzilini to'g'ri bering.", "Input/output", "easy", "scanf qiymatni o'zgaruvchiga yozishi uchun uning manzili & bilan beriladi.", '#include <stdio.h>\nint main() {\n    int yosh;\n    scanf("%d", ____);\n    return 0;\n}', "&yosh"),
    question("Ekranga matn chiqaruvchi funksiyani to'g'rilang.", "Input/output", "easy", "printf C tilida ekranga ma'lumot chiqaradi.", '#include <stdio.h>\nint main() {\n    ____("Salom, C!");\n    return 0;\n}', "printf"),
    question("int qiymatni chiqarish formatini to'g'rilang.", "Input/output", "easy", "int uchun printf format belgisi %d hisoblanadi.", '#include <stdio.h>\nint main() {\n    int son = 25;\n    printf("Son: %____", son);\n    return 0;\n}', "d"),
    question("float qiymatni olish formatini to'g'rilang.", "Input/output", "easy", "scanf funksiyasida float uchun %f ishlatiladi.", '#include <stdio.h>\nint main() {\n    float narx;\n    scanf("%____", &narx);\n    return 0;\n}', "f"),
    question("double qiymatni olish formatini to'g'rilang.", "Input/output", "medium", "double qiymatni scanf orqali olishda %lf ishlatiladi.", '#include <stdio.h>\nint main() {\n    double massa;\n    scanf("%____", &massa);\n    return 0;\n}', "lf"),
    question("O'nli qiymat uchun o'zgaruvchi turini to'g'rilang.", "Ma'lumot turlari", "easy", "float o'nli kasr qiymatlarni saqlash uchun ishlatiladi.", '#include <stdio.h>\nint main() {\n    ____ harorat = 36.6f;\n    printf("%.1f", harorat);\n    return 0;\n}', "float"),
    question("Yuqori aniqlikdagi o'nli tur nomini to'g'rilang.", "Ma'lumot turlari", "easy", "double float ga qaraganda odatda yuqoriroq aniqlik beradi.", '#include <stdio.h>\nint main() {\n    ____ pi = 3.1415926535;\n    printf("%f", pi);\n    return 0;\n}', "double"),
    question("Butun son o'zgaruvchisi turini to'g'rilang.", "Ma'lumot turlari", "easy", "int butun sonlar uchun ishlatiladi.", '#include <stdio.h>\nint main() {\n    ____ talabalar = 30;\n    printf("%d", talabalar);\n    return 0;\n}', "int"),
    question("main funksiyasining qaytish turini to'g'rilang.", "Input/output", "easy", "Odatdagi C dasturida main funksiyasi int qiymat qaytaradi.", '#include <stdio.h>\n____ main() {\n    printf("Dastur");\n    return 0;\n}', "int"),

    # if, else if, else: 11-22
    question("Shart operatorining kalit so'zini to'g'rilang.", "if", "easy", "C tilida shart tekshirish if bilan boshlanadi.", 'int yosh = 20;\n____ (yosh >= 18) {\n    printf("Voyaga yetgan");\n}', "if"),
    question("if shartidagi taqqoslash operatorini to'g'rilang.", "if", "easy", "Tenglikni tekshirish uchun == ishlatiladi, = esa qiymat beradi.", 'int son = 10;\nif (son ____ 10) {\n    printf("Teng");\n}', "=="),
    question("if blokini to'g'ri yoping.", "if", "easy", "C kod bloklari jingalak qavs bilan yopiladi.", 'int son = 5;\nif (son > 0) {\n    printf("Musbat");\n____', "}"),
    question("Katta yoki teng operatorini to'g'rilang.", "if", " >= qiymat katta yoki tengligini tekshiradi.", 'int ball = 70;\nif (ball ____ 60) {\n    printf("Otdi");\n}', ">="),
    question("Mantiqiy AND operatorini to'g'rilang.", "if", "Ikki shart bir vaqtda rost bo'lishi uchun && ishlatiladi.", 'int yosh = 20;\nint hujjat = 1;\nif (yosh >= 18 ____ hujjat == 1) {\n    printf("Kirish mumkin");\n}', "&&"),
    question("Mantiqiy OR operatorini to'g'rilang.", "if", "Kamida bitta shart rost bo'lishi uchun || ishlatiladi.", 'int kun = 6;\nif (kun == 6 ____ kun == 7) {\n    printf("Dam olish");\n}', "||"),
    question("Shart rost bo'lmaganda ishlaydigan blokni to'g'rilang.", "else", "else if shartlari bajarilmaganda bajariladigan blokdir.", 'int son = -2;\nif (son > 0) {\n    printf("Musbat");\n} ____ {\n    printf("Musbat emas");\n}', "else"),
    question("Ikkinchi shartni tekshiruvchi kalit so'zlarni to'g'rilang.", "else if", "Bir nechta shartni ketma-ket tekshirish uchun else if ishlatiladi.", 'int ball = 75;\nif (ball >= 90) {\n    printf("A");\n} ____ (ball >= 70) {\n    printf("B");\n}', "else if"),
    question("if va else if orasidagi qavsni to'g'rilang.", "else if", "Har bir shart qavs ichida yoziladi.", 'int son = 0;\nif (son > 0) {\n    printf("Musbat");\n} else if ____ {\n    printf("Manfiy");\n}', "(son < 0)"),
    question("if shartining tanasini to'g'ri belgilang.", "if", "if dan keyingi bajariladigan buyruqlar jingalak qavs ichida bo'ladi.", 'if (1) ____\n    printf("Rost");\n}', "{"),
    question("Teng emas operatorini to'g'rilang.", "if", "Teng emaslikni tekshirish uchun != ishlatiladi.", 'int parol = 1234;\nif (parol ____ 0) {\n    printf("Kiritildi");\n}', "!="),
    question("Qiymatni tekshiruvchi shartni to'g'rilang.", "if", "if ichida mantiqiy ifoda yoziladi va u qavs bilan o'raladi.", 'int aktiv = 1;\n____ (aktiv) {\n    printf("Faol");\n}', "if"),

    # switch / case: 23-30
    question("Bir nechta aniq qiymatni tanlash uchun operatorni to'g'rilang.", "switch case", "easy", "switch bitta ifodaning turli qiymatlarini case orqali tekshiradi.", 'int tanlov = 2;\n____ (tanlov) {\n    case 1: printf("Bir"); break;\n}', "switch"),
    question("switch ichidagi qiymat tarmog'ini to'g'rilang.", "switch case", "easy", "Har bir mumkin bo'lgan qiymat case bilan yoziladi.", 'int kun = 1;\nswitch (kun) {\n    ____ 1: printf("Dushanba"); break;\n}', "case"),
    question("case bajarilgach keyingi case ga o'tishni to'xtating.", "switch case", "break switch bajarilishini shu joyda to'xtatadi.", 'int x = 1;\nswitch (x) {\n    case 1:\n        printf("Bir");\n        ____;\n}', "break"),
    question("Hech bir case mos kelmaganda ishlaydigan qismni to'g'rilang.", "switch case", "default hech bir case mos kelmaganda ishlaydi.", 'int rang = 9;\nswitch (rang) {\n    case 1: printf("Qizil"); break;\n    ____: printf("Nomalum");\n}', "default"),
    question("switch sintaksisidagi qavsni to'g'rilang.", "switch case", "switch operatorining tanasi jingalak qavs ichida yoziladi.", 'int tanlov = 1;\nswitch (tanlov) ____\n    case 1: printf("OK"); break;\n}', "{"),
    question("case qiymatidan keyingi belgini to'g'rilang.", "switch case", "case qiymatidan keyin ikki nuqta qo'yiladi.", 'int oy = 1;\nswitch (oy) {\n    case 1____\n        printf("Yanvar");\n}', ":"),
    question("switch blokini to'g'ri yakunlang.", "switch case", "switch bloki yopuvchi jingalak qavs bilan tugaydi.", 'switch (1) {\n    case 1: printf("Bir"); break;\n____', "}"),
    question("case ichidagi chiqishni to'xtatish buyrug'ini to'g'rilang.", "switch case", "break bo'lmasa keyingi case lar ham bajarilishi mumkin.", 'char belgi = 97;\nswitch (belgi) {\n    case 97:\n        printf("A");\n        ____;\n}', "break"),

    # goto: 31-34
    question("Belgilangan qatorga o'tish operatorini to'g'rilang.", "goto", "medium", "goto ko'rsatilgan label nomiga o'tadi.", 'int x = 0;\nif (x == 0) {\n    ____ tugash;\n}\nprintf("Bajarilmaydi");\ntugash:\nprintf("Tugadi");', "goto"),
    question("goto uchun label yozilishini to'g'rilang.", "goto", "easy", "Label nomidan keyin ikki nuqta qo'yiladi.", 'int x = 1;\n____:\nprintf("Boshlanish");', "boshlash:"),
    question("goto o'tadigan label nomini to'g'rilang.", "goto", "medium", "goto va label nomi bir xil bo'lishi kerak.", 'goto ____;\nprintf("Bu qator otkaziladi");\nfinish:\nprintf("Tugadi");', "finish"),
    question("goto bilan o'tish buyrug'ini nuqta-vergul bilan yakunlang.", "goto", "goto buyrug'i ham nuqta-vergul bilan tugaydi.", 'int x = 0;\nif (x == 0) {\n    goto tugash____\n}\ntugash:\nprintf("OK");', ";"),

    # for: 35-41
    question("for siklining kalit so'zini to'g'rilang.", "for", "easy", "Takrorlanishlar soni ma'lum bo'lganda for qulay.", '____ (int i = 0; i < 5; i++) {\n    printf("%d ", i);\n}', "for"),
    question("for siklining boshlang'ich qiymatini to'g'rilang.", "for", "i = 0 sikl hisoblagichini boshlang'ich qiymatga o'rnatadi.", 'for (int i ____ 0; i < 3; i++) {\n    printf("%d", i);\n}', "="),
    question("for siklining davom etish shartini to'g'rilang.", "for", "i < 10 sharti i 10 ga yetguncha siklni davom ettiradi.", 'for (int i = 0; i ____ 10; i++) {\n    printf("%d ", i);\n}', "<"),
    question("for hisoblagichini oshirish operatorini to'g'rilang.", "for", "i++ har bir aylanishdan keyin i ni bittaga oshiradi.", 'for (int i = 0; i < 5; i____) {\n    printf("%d", i);\n}', "++"),
    question("for sikli tanasining ochuvchi qavsini to'g'rilang.", "for", "Sikl tanasi jingalak qavs bilan ochiladi.", 'for (int i = 0; i < 3; i++) ____\n    printf("%d", i);\n}', "{"),
    question("for sikli ichida keyingi aylanishga o'tish buyrug'ini to'g'rilang.", "for", "continue joriy aylanishning qolgan qismini o'tkazib yuboradi.", 'for (int i = 0; i < 5; i++) {\n    if (i == 2) ____;\n    printf("%d", i);\n}', "continue"),
    question("for siklini erta tugatish buyrug'ini to'g'rilang.", "for", "break siklni darhol to'xtatadi.", 'for (int i = 0; i < 10; i++) {\n    if (i == 5) ____;\n}', "break"),

    # while: 42-46
    question("Shart bajarilguncha takrorlanuvchi siklni to'g'rilang.", "while", "easy", "while shart rost bo'lib turganida kodni takrorlaydi.", 'int i = 0;\n____ (i < 3) {\n    printf("%d", i);\n    i++;\n}', "while"),
    question("while shartidagi taqqoslashni to'g'rilang.", "while", "Sikl 5 dan kichik qiymatlar uchun ishlashi kerak.", 'int i = 0;\nwhile (i ____ 5) {\n    i++;\n}', "<"),
    question("while siklida hisoblagichni oshiring.", "while", "Hisoblagich o'zgarmasa, sikl cheksiz davom etishi mumkin.", 'int i = 1;\nwhile (i <= 3) {\n    printf("%d", i);\n    i____;\n}', "++"),
    question("while siklini erta tugatish buyrug'ini to'g'rilang.", "while", "break while siklini darhol tugatadi.", 'int son;\nwhile (1) {\n    scanf("%d", &son);\n    if (son == 0) ____;\n}', "break"),
    question("while siklida keyingi aylanishga o'tish buyrug'ini to'g'rilang.", "while", "continue while siklining keyingi aylanishiga o'tadi.", 'int i = 0;\nwhile (i < 5) {\n    i++;\n    if (i == 3) ____;\n    printf("%d", i);\n}', "continue"),

    # do while: 47-50
    question("Kamida bir marta bajariladigan siklni to'g'rilang.", "do while", "easy", "do while shartni oxirida tekshiradi, shuning uchun tana kamida bir marta bajariladi.", 'int i = 0;\n____ {\n    printf("%d", i);\n    i++;\n} while (i < 3);', "do"),
    question("do while siklining shart operatorini to'g'rilang.", "do while", "do blokidan keyin while sharti yoziladi.", 'int i = 0;\ndo {\n    i++;\n} ____ (i < 3);', "while"),
    question("do while siklining shart qavsini to'g'rilang.", "do while", "while sharti qavs ichida yoziladi.", 'int i = 0;\ndo {\n    i++;\n} while ____ i < 3);', "("),
    question("do while qatorining yakuniy belgisini to'g'rilang.", "do while", "do while konstruksiyasi nuqta-vergul bilan tugaydi.", 'int i = 0;\ndo {\n    i++;\n} while (i < 3)____', ";"),
]


class Command(BaseCommand):
    help = "C asosiy mavzulari uchun 50 ta kod xatosini tuzatish testini yaratadi."

    def handle(self, *args, **options):
        course = Course.objects.filter(slug="c-dasturlash-tili").first()
        lesson = Lesson.objects.filter(course=course, order=2).first() if course else None
        if not course or not lesson:
            raise CommandError("C kursi yoki 2-dars topilmadi.")

        quiz, _ = Quiz.objects.update_or_create(
            slug="c-asosiy-mavzular-kod-xatosini-tuzatish-50-test",
            defaults={
                "title": "C asosiy mavzular: Kod xatosini tuzatish — 50 ta test",
                "description": "Input/output, ma'lumot turlari, shart operatorlari, switch/case, goto va sikllar bo'yicha kod blankalarini to'ldiring.",
                "lesson": lesson,
                "course": course,
                "category": "Dasturlash",
                "topic": "C dasturlash tili asoslari",
                "quiz_type": "code_fix",
                "time_limit": 1800,
                "pass_score": 60,
                "randomize_questions": True,
                "published": True,
            },
        )
        quiz.questions.all().delete()
        Question.objects.bulk_create([
            Question(quiz=quiz, order=index, **item)
            for index, item in enumerate(QUESTIONS, 1)
        ])
        self.stdout.write(self.style.SUCCESS(f"'{quiz.title}' yaratildi: {len(QUESTIONS)} ta savol."))
