from django.core.management.base import BaseCommand

from apps.courses.models import Course


DESCRIPTIONS = {
    "telegram-bot": """Telegram botlarni noldan yaratishni o‘rganing.

Ushbu kursda Python va Aiogram yordamida foydali, tezkor va interaktiv Telegram botlar quramiz. Darslar amaliy loyihalar asosida tuzilgan: bot foydalanuvchini kutib oladi, buyruqlarni qayta ishlaydi, tugmalar va menyularni ko‘rsatadi, ma’lumotlarni saqlaydi va API’lar bilan ishlaydi.

Kurs davomida:
- Telegram Bot API va bot arxitekturasi
- Aiogram’da handler, state va keyboardlar
- Inline tugmalar va callbacklar
- Foydalanuvchi ma’lumotlari bilan ishlash
- Ma’lumotlar bazasiga ulash
- Botni serverga joylash va webhook bilan ishlatish

Kurs yakunida siz real xizmat, o‘quv yoki biznes loyihasi uchun Telegram bot yaratish ko‘nikmasiga ega bo‘lasiz.""",
    "html-for-beginner": """Web dasturlashga HTML asoslaridan start bering.

HTML for Beginner kursi web sahifaning tuzilishini noldan tushuntiradi. Siz matn, sarlavha, havola, rasm, ro‘yxat, jadval va forma kabi elementlarni to‘g‘ri ishlatib, tartibli web sahifalar yaratishni o‘rganasiz.

Kurs davomida:
- HTML hujjatining asosiy tuzilmasi
- Semantik teglar va sahifa bo‘limlari
- Havolalar, rasmlar va multimedia
- Tartibli va tartibsiz ro‘yxatlar
- Jadvallar va formalar
- HTML faylini brauzerda tekshirish
- CSS’ga tayyor, toza markup yozish

Har bir mavzu amaliy misollar va testlar bilan mustahkamlanadi. Kurs HTML’ni birinchi marta o‘rganayotganlar uchun mos.""",
    "python-beginner": """Python dasturlash tilini noldan, sodda va amaliy usulda o‘rganing.

Python Beginner kursi dasturlashga endi kirib kelayotgan o‘quvchilar uchun tuzilgan. Darslarda kod yozish muhiti, o‘zgaruvchilar, ma’lumot turlari, operatorlar, shartlar, sikllar, funksiyalar va ma’lumotlar tuzilmalari bosqichma-bosqich tushuntiriladi.

Kurs davomida:
- Python sintaksisi va kod yozish qoidalari
- O‘zgaruvchilar, satrlar, sonlar va boolean qiymatlar
- Shart operatorlari va takrorlanuvchi jarayonlar
- List, tuple, set va dictionary bilan ishlash
- Funksiyalar va kodni tartibli tashkil qilish
- Xatolarni topish va kodni tekshirish
- Kichik amaliy dasturlar yaratish

Kurs yakunida siz mustaqil ravishda sodda Python dasturlarini yozish va keyingi dasturlash mavzulariga tayyor bo‘lasiz.""",
}


class Command(BaseCommand):
    help = "Boshlang'ich kurslarning tavsiflarini yangilaydi."

    def handle(self, *args, **options):
        for slug, description in DESCRIPTIONS.items():
            updated = Course.objects.filter(slug=slug).update(short_description=description)
            if updated:
                self.stdout.write(self.style.SUCCESS(f"{slug}: tavsif yangilandi"))
            else:
                self.stdout.write(self.style.WARNING(f"{slug}: kurs topilmadi"))
