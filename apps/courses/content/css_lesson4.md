# 4-Dars: CSS Box Model — o‘lcham, oraliq va chegara

## Dars maqsadi

Ushbu darsdan keyin siz:

- CSS Box Model nima ekanini aniq tushuntira olasiz;
- `content`, `padding`, `border` va `margin` farqini bilasiz;
- `width` va `height` qanday hisoblanishini tushunasiz;
- `box-sizing: border-box` nima uchun kerakligini bilasiz;
- elementlar orasidagi masofani to‘g‘ri boshqara olasiz;
- `border-radius`, `box-shadow` va `outline` bilan ishlay olasiz;
- natijani brauzerda ko‘rib, kod bilan taqqoslay olasiz;
- amaliy kurs cardini Box Model yordamida yarata olasiz.

---

## 1. Box Model nima?

Brauzer HTML’dagi har bir elementni to‘rt qavatli quti sifatida hisoblaydi. Bu tizim **CSS Box Model** deb ataladi.

```text
margin  — tashqi bo‘sh joy
border  — chegara
padding — ichki bo‘sh joy
content — matn yoki ichki element
```

Har bir `div`, `p`, `button`, `img` yoki card aslida shu quti modeliga ega.

<svg viewBox="0 0 760 340" role="img" aria-label="CSS Box Model qatlamlari" style="width:100%;height:auto;background:#f8fafc;border:1px solid #cbd5e1;border-radius:16px;padding:18px;box-sizing:border-box">
  <rect x="25" y="25" width="710" height="285" rx="18" fill="#fef3c7" stroke="#f59e0b" stroke-width="3"/>
  <rect x="90" y="70" width="580" height="195" rx="14" fill="#dbeafe" stroke="#2563eb" stroke-width="3"/>
  <rect x="155" y="112" width="450" height="110" rx="10" fill="#ffffff" stroke="#64748b" stroke-width="3"/>
  <rect x="215" y="140" width="330" height="55" rx="8" fill="#2563eb"/>
  <text x="380" y="174" text-anchor="middle" fill="#ffffff" font-size="20" font-weight="700" font-family="sans-serif">CONTENT</text>
  <text x="380" y="52" text-anchor="middle" fill="#92400e" font-size="18" font-weight="700" font-family="sans-serif">MARGIN — tashqi masofa</text>
  <text x="380" y="96" text-anchor="middle" fill="#1e3a8a" font-size="18" font-weight="700" font-family="sans-serif">PADDING — ichki masofa</text>
  <text x="380" y="250" text-anchor="middle" fill="#475569" font-size="17" font-weight="700" font-family="sans-serif">BORDER — chegara</text>
</svg>

### Qatlamlarning vazifasi

- **Content** — matn, rasm yoki ichki element joylashgan asosiy qism;
- **Padding** — content bilan border orasidagi ichki bo‘sh joy;
- **Border** — elementni o‘rab turuvchi chegara;
- **Margin** — elementning boshqa elementlardan tashqi masofasi.

---

## 2. Content va `width` / `height`

`width` va `height` odatda content qismning o‘lchamini bildiradi.

```css
.box {
  width: 260px;
  height: 120px;
  background-color: #2563eb;
  color: white;
}
```

### Natija

<div style="width:260px;height:120px;display:flex;align-items:center;justify-content:center;margin:16px 0;border-radius:12px;background:#2563eb;color:white;font-weight:700">260px × 120px content</div>

`width` va `height`ga birlik berish mumkin:

```css
.fixed-box {
  width: 300px;
  height: 160px;
}

.fluid-box {
  width: 100%;
  min-height: 120px;
}
```

### Qaysi birlikni tanlash kerak?

- `px` — aniq o‘lcham uchun;
- `%` — ota elementga nisbatan;
- `rem` — umumiy responsive o‘lcham uchun;
- `vw` va `vh` — viewportga nisbatan;
- `min-width` va `max-width` — elementni chegaralash uchun.

```css
.content {
  width: min(100%, 720px);
  min-height: 200px;
}
```

Natijada element kichik ekranda 100% kenglikni, katta ekranda esa 720px gacha bo‘lgan kenglikni egallaydi.

---

## 3. Padding — ichki masofa

`padding` content va border orasidagi masofani boshqaradi.

```css
.padding-box {
  padding: 24px;
  background-color: #dbeafe;
  border: 2px solid #2563eb;
}
```

### Natija

<div style="display:inline-block;margin:16px 0;padding:24px;border:2px solid #2563eb;border-radius:12px;background:#dbeafe;color:#1e3a8a;font-weight:700">Matn va chegara orasida 24px</div>

Paddingni to‘rt tomonga alohida berish mumkin:

```css
.box {
  padding-top: 12px;
  padding-right: 20px;
  padding-bottom: 28px;
  padding-left: 20px;
}
```

Shorthand yozuvlar:

```css
/* Barcha tomon 20px */
.one { padding: 20px; }

/* Yuqori-past 12px, chap-o‘ng 24px */
.two { padding: 12px 24px; }

/* Yuqori 8px, chap-o‘ng 20px, past 16px */
.three { padding: 8px 20px 16px; }

/* Yuqori, o‘ng, past, chap */
.four { padding: 8px 16px 20px 24px; }
```

Shorthand tartibini eslab qoling: **top → right → bottom → left**. Buni soat yo‘nalishi kabi tasavvur qiling.

---

## 4. Border — chegara

Border uchta asosiy qismdan tuziladi:

```css
.border-box {
  border-width: 2px;
  border-style: solid;
  border-color: #2563eb;
}
```

Ko‘pincha qisqa yozuv ishlatiladi:

```css
.card {
  border: 1px solid #dbeafe;
}
```

### Border turlari

```css
.solid { border: 2px solid #2563eb; }
.dashed { border: 2px dashed #06b6d4; }
.dotted { border: 3px dotted #8b5cf6; }
.none { border: none; }
```

### Natija

<div style="display:flex;flex-wrap:wrap;gap:12px;margin:16px 0">
  <div style="padding:16px;border:2px solid #2563eb;border-radius:10px;color:#1e3a8a">solid</div>
  <div style="padding:16px;border:2px dashed #06b6d4;border-radius:10px;color:#0e7490">dashed</div>
  <div style="padding:16px;border:3px dotted #8b5cf6;border-radius:10px;color:#6d28d9">dotted</div>
</div>

Har bir tomonga alohida border berish mumkin:

```css
.accent-card {
  border-top: 4px solid #2563eb;
  border-right: 1px solid #dbeafe;
  border-bottom: 1px solid #dbeafe;
  border-left: 1px solid #dbeafe;
}
```

---

## 5. `border-radius` — yumaloq burchaklar

```css
.rounded {
  border-radius: 16px;
}

.pill {
  border-radius: 999px;
}

.circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}
```

### Natija

<div style="display:flex;align-items:center;flex-wrap:wrap;gap:16px;margin:16px 0">
  <div style="width:110px;height:70px;display:flex;align-items:center;justify-content:center;border-radius:16px;background:#2563eb;color:white;font-size:13px">16px</div>
  <div style="padding:12px 24px;border-radius:999px;background:#06b6d4;color:#083344;font-size:13px;font-weight:700">PILL BUTTON</div>
  <div style="width:80px;height:80px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#8b5cf6;color:white;font-size:13px">50%</div>
</div>

Radiusni har bir burchak uchun alohida sozlash mumkin:

```css
.custom-radius {
  border-radius: 24px 4px 24px 4px;
}
```

---

## 6. Margin — tashqi masofa

`margin` elementning tashqi masofasini boshqaradi.

```css
.first-card {
  margin-bottom: 24px;
}

.center-card {
  width: 320px;
  margin: 0 auto;
}
```

`margin: 0 auto` block elementni gorizontal markazga qo‘yadi, agar uning kengligi berilgan bo‘lsa.

Shorthand:

```css
/* Barcha tomon 16px */
.one { margin: 16px; }

/* Yuqori-past 24px, chap-o‘ng 0 */
.two { margin: 24px 0; }

/* Yuqori 8px, chap-o‘ng 20px, past 16px */
.three { margin: 8px 20px 16px; }

/* Yuqori, o‘ng, past, chap */
.four { margin: 8px 16px 20px 24px; }
```

### Padding va margin farqi

```css
.example {
  padding: 20px; /* quti ichidagi masofa */
  margin: 20px;  /* quti tashqarisidagi masofa */
}
```

Padding fon rangining ichida ko‘rinadi. Margin esa element tashqarisida bo‘ladi va odatda elementning fon rangini egallamaydi.

<div style="margin:16px 0;padding:20px;border:3px solid #2563eb;border-radius:14px;background:#dbeafe;color:#1e3a8a">
  <div style="padding:18px;border:2px dashed #06b6d4;border-radius:10px;background:white;color:#0f172a;text-align:center;font-weight:700">Padding: ichki bo‘sh joy</div>
</div>

---

## 7. Box sizing va haqiqiy o‘lcham

Standart holatda CSS’da `width` faqat content kengligini bildiradi. Padding va border unga qo‘shiladi.

```css
.standard-box {
  width: 300px;
  padding: 20px;
  border: 4px solid #2563eb;
}
```

Standart hisob:

```text
Umumiy kenglik = width + chap padding + o‘ng padding + chap border + o‘ng border
Umumiy kenglik = 300 + 20 + 20 + 4 + 4 = 348px
```

Shuning uchun ko‘p loyihalarda quyidagi qoida ishlatiladi:

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

`border-box` bilan berilgan `width` ichiga padding va border ham kiradi. Yuqoridagi quti tashqi tomondan aynan 300px bo‘ladi.

```css
.predictable-box {
  box-sizing: border-box;
  width: 300px;
  padding: 20px;
  border: 4px solid #2563eb;
}
```

### Natija

<div style="display:flex;flex-wrap:wrap;gap:16px;margin:16px 0">
  <div style="box-sizing:content-box;width:150px;padding:20px;border:4px solid #ef4444;border-radius:10px;color:#991b1b;font-size:13px;text-align:center">content-box<br/>tashqi kenglik kattaroq</div>
  <div style="box-sizing:border-box;width:150px;padding:20px;border:4px solid #2563eb;border-radius:10px;color:#1e3a8a;font-size:13px;text-align:center">border-box<br/>aniq 150px</div>
</div>

> Amaliy tavsiya: reset CSS’ning boshida `box-sizing: border-box` qoidasini yozib qo‘ying. Bu card va layout o‘lchamlarini oldindan taxmin qilishni osonlashtiradi.

---

## 8. `box-shadow` — soya

Soya card va tugmalarga chuqurlik beradi.

```css
.soft-card {
  box-shadow: 0 10px 30px rgb(15 23 42 / 12%);
}
```

`box-shadow` tarkibi:

```text
horizontal-offset vertical-offset blur spread color
```

```css
.shadow-example {
  box-shadow: 4px 6px 18px 0 rgb(15 23 42 / 20%);
}
```

- `4px` — o‘ngga siljish;
- `6px` — pastga siljish;
- `18px` — xiralik;
- `0` — tarqalish;
- oxirgi qiymat — soya rangi.

Ichki soya uchun `inset` ishlatiladi:

```css
.inset-shadow {
  box-shadow: inset 0 2px 8px rgb(15 23 42 / 12%);
}
```

Bir nechta soya yozish mumkin:

```css
.layered-shadow {
  box-shadow:
    0 2px 4px rgb(15 23 42 / 8%),
    0 12px 30px rgb(37 99 235 / 14%);
}
```

### Natija

<div style="display:flex;flex-wrap:wrap;gap:16px;margin:16px 0">
  <div style="width:180px;padding:24px;border-radius:16px;background:white;box-shadow:0 10px 30px rgb(15 23 42 / 16%);color:#0f172a;text-align:center">Soft shadow</div>
  <div style="width:180px;padding:24px;border-radius:16px;background:#dbeafe;box-shadow:inset 0 2px 8px rgb(15 23 42 / 16%);color:#1e3a8a;text-align:center">Inset shadow</div>
</div>

---

## 9. `outline` va `overflow`

`outline` borderga o‘xshaydi, lekin layout o‘lchamiga qo‘shilmaydi.

```css
button:focus-visible {
  outline: 3px solid #22d3ee;
  outline-offset: 4px;
}
```

Bu klaviatura bilan foydalanuvchi tugmaga kelganda qaysi element faol ekanini ko‘rsatadi. Accessibility uchun focus outline’ni butunlay olib tashlamang.

```css
/* Bunday qilish tavsiya etilmaydi */
button:focus {
  outline: none;
}
```

### `overflow`

Content qutiga sig‘masa, `overflow` nima bo‘lishini belgilaydi.

```css
.hidden-content {
  height: 80px;
  overflow: hidden;
}

.scroll-content {
  height: 120px;
  overflow: auto;
}
```

Rasm card’dan chiqib ketmasligi uchun:

```css
.image-card {
  overflow: hidden;
  border-radius: 18px;
}
```

---

## 10. Amaliy loyiha: CSS kurs cardi

Quyidagi loyiha darsda o‘rgangan Box Model xususiyatlarini birlashtiradi.

### HTML

```html
<article class="course-card">
  <div class="course-card__icon" aria-hidden="true">CSS</div>
  <p class="course-card__label">WEB DASTURLASH</p>
  <h2 class="course-card__title">CSS for Beginner</h2>
  <p class="course-card__text">
    Ranglar, layout va chiroyli web interfeyslar yaratishni o‘rganing.
  </p>
  <a class="course-card__link" href="#start">Kursni boshlash →</a>
</article>
```

### CSS

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}

.course-card {
  width: min(100%, 360px);
  margin: 24px auto;
  padding: 24px;
  overflow: hidden;
  border: 1px solid #dbeafe;
  border-radius: 20px;
  background: #ffffff;
  box-shadow: 0 12px 32px rgb(15 23 42 / 10%);
}

.course-card__icon {
  width: 64px;
  height: 64px;
  display: grid;
  place-items: center;
  margin-bottom: 20px;
  border-radius: 16px;
  background: linear-gradient(135deg, #2563eb, #06b6d4);
  color: white;
  font-size: 18px;
  font-weight: 800;
}

.course-card__label {
  margin: 0 0 8px;
  color: #2563eb;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.14em;
}

.course-card__title {
  margin: 0;
  color: #0f172a;
  font-size: 26px;
  line-height: 1.15;
}

.course-card__text {
  margin: 14px 0 22px;
  color: #64748b;
  line-height: 1.7;
}

.course-card__link {
  display: inline-block;
  padding: 11px 16px;
  border-radius: 10px;
  background: #2563eb;
  color: white;
  font-weight: 700;
  text-decoration: none;
}

.course-card__link:hover {
  background: #1d4ed8;
}
```

### Natija

<div style="width:min(100%,360px);margin:20px 0;padding:24px;overflow:hidden;border:1px solid #dbeafe;border-radius:20px;background:#ffffff;box-shadow:0 12px 32px rgb(15 23 42 / 10%)">
  <div style="width:64px;height:64px;display:grid;place-items:center;margin-bottom:20px;border-radius:16px;background:linear-gradient(135deg,#2563eb,#06b6d4);color:white;font-size:18px;font-weight:800">CSS</div>
  <p style="margin:0 0 8px;color:#2563eb;font-size:11px;font-weight:800;letter-spacing:.14em">WEB DASTURLASH</p>
  <h2 style="margin:0;color:#0f172a;font-size:26px;line-height:1.15">CSS for Beginner</h2>
  <p style="margin:14px 0 22px;color:#64748b;line-height:1.7">Ranglar, layout va chiroyli web interfeyslar yaratishni o‘rganing.</p>
  <a href="#start" style="display:inline-block;padding:11px 16px;border-radius:10px;background:#2563eb;color:white;font-weight:700;text-decoration:none">Kursni boshlash →</a>
</div>

Kodni o‘zgartirib quyidagilarni sinab ko‘ring:

1. Card paddingini `24px`dan `32px`ga o‘zgartiring.
2. Border rangini cyan qiling.
3. `border-radius`ni 8px qilib ko‘ring.
4. Soya xiraligini kamaytiring.
5. Icon uchun SVG ishlating.

---

## 11. Ko‘p uchraydigan xatolar

### `width`ga padding qo‘shilib ketishi

`box-sizing: border-box`ni global reset’ga qo‘shing.

### Margin o‘rniga padding ishlatish

Element ichidagi masofa kerak bo‘lsa padding, boshqa elementdan uzoqlik kerak bo‘lsa margin ishlating.

### `margin: auto` ishlamayapti

Gorizontal markazlash uchun block elementga kenglik bering:

```css
.center {
  width: 320px;
  margin-inline: auto;
}
```

### Kichik ekranda card tashqariga chiqmoqda

```css
img {
  max-width: 100%;
  height: auto;
}

.card {
  width: min(100%, 360px);
}
```

### Soya juda kuchli

Soya dizaynni to‘ldirishi kerak, elementni bosib ketmasligi kerak. Alpha qiymatini kichikroq qiling:

```css
box-shadow: 0 12px 30px rgb(15 23 42 / 10%);
```

---

## 12. Mustahkamlash topshiriqlari

### Topshiriq 1: Box Model tajribasi

Bitta `div` yarating. Unga 200px kenglik, 20px padding, 5px border va 30px margin bering. `content-box` va `border-box` farqini o‘lchang.

### Topshiriq 2: Uch xil button

Padding va border-radius yordamida primary, outline va pill buttonlar yarating. Har birining hover holatini sozlang.

### Topshiriq 3: Cardlar qatori

Uchta kurs cardi yarating. Cardlarning padding, border, radius va shadow qiymatlarini bir xil qiling.

### Topshiriq 4: Focus holati

Button va linklarga `:focus-visible` holati qo‘shing. Klaviatura bilan sahifani aylanib tekshiring.

### Topshiriq 5: Natijani tushuntirish

O‘zingiz yaratgan card uchun uning umumiy kengligi qanday hisoblanganini yozib chiqing.

---

## 13. Uyga vazifa: responsive profile card

Profil card yarating. Unda:

- SVG avatar;
- ism va kasb;
- qisqa bio;
- ikkita tugma;
- padding, margin, border va shadow;
- `box-sizing: border-box`;
- telefon ekraniga mos kenglik;
- tugmalarda `:hover` va `:focus-visible`;
- koddan keyin ko‘rinadigan natijani tekshirish

bo‘lsin.

Card o‘lchamlarini `width: min(100%, 420px)` orqali boshqaring. Natija ekran kengligidan oshib ketmasin.

---

## Dars xulosasi

Bugun CSS Box Model’ning barcha qatlamlarini — content, padding, border va marginni o‘rgandik. `box-sizing: border-box` yordamida element o‘lchamini oldindan aniq hisoblashni, `border-radius`, `box-shadow`, `outline` va `overflow` yordamida cardlarni chiroyli qilishni ko‘rdik. Har bir asosiy koddan keyin uning natijasini ham ko‘rib, kod va ko‘rinish o‘rtasidagi bog‘lanishni mustahkamladik.

Keyingi darsda selectorlar, pseudo-classlar va elementlarni aniq tanlash usullarini chuqurroq o‘rganamiz.
