# 2-Dars: Ranglar, fonlar va gradientlar

## Dars maqsadi

Ushbu darsdan keyin siz:

- CSS’da rang berishning asosiy usullarini tushuntira olasiz;
- nomlangan rang, HEX, RGB, RGBA, HSL va HSLA qiymatlaridan foydalana olasiz;
- rang shaffofligini alpha kanali orqali boshqara olasiz;
- `background-color`, `background-image`, `background-size` va `background-position` xususiyatlarini ishlata olasiz;
- linear va radial gradient yaratishingiz mumkin bo‘ladi;
- hover holatlari uchun rang o‘tishlarini sozlay olasiz;
- SVG ichida gradient va ranglardan foydalana olasiz;
- kontrast va o‘qilishi yaxshi bo‘lgan dizayn yaratish qoidalarini bilasiz;
- rangli hero section va kurs card yaratishingiz mumkin bo‘ladi.

---

## 1. Rang dizaynning eng muhim qismi

Rang web sahifadagi kayfiyatni, ma’lumotlar ierarxiyasini va foydalanuvchi e’tiborini boshqaradi. Masalan:

- ko‘k rang — ishonch, texnologiya va xotirjamlik;
- yashil rang — muvaffaqiyat va tasdiq;
- sariq rang — ogohlantirish va e’tibor;
- qizil rang — xato yoki xavf;
- binafsha rang — kreativlik va premium ko‘rinish;
- kulrang — ikkilamchi matn va neytral fon.

Rangni shunchaki chiroyli bo‘lgani uchun emas, uning vazifasini o‘ylab tanlang. Asosiy matn o‘qilishi oson, tugmalar esa fondan ajralib turishi kerak.

```css
body {
  background-color: #f8fafc;
  color: #0f172a;
}

.primary-button {
  background-color: #2563eb;
  color: #ffffff;
}

.success-message {
  background-color: #dcfce7;
  color: #166534;
}

.error-message {
  background-color: #fee2e2;
  color: #991b1b;
}
```

---

## 2. CSS’da rang yozish usullari

### 2.1. Rang nomi

CSS’da yuzlab tayyor rang nomlari mavjud.

```css
.box-one {
  color: white;
  background-color: navy;
}

.box-two {
  color: black;
  background-color: gold;
}
```

Bu usul tezkor tajriba uchun qulay, lekin professional dizaynda odatda aniq HEX, RGB yoki HSL qiymatlaridan foydalaniladi.

### 2.2. HEX ranglar

HEX — o‘n oltilik sanoq sistemasidagi rang yozuvi. U `#` belgisi va oltita belgidan iborat bo‘ladi.

```css
.academy-blue {
  color: #2563eb;
}

.academy-dark {
  background-color: #0f172a;
}

.academy-cyan {
  border-color: #06b6d4;
}
```

HEX qiymatining tuzilishi:

```text
#RRGGBB
```

- `RR` — qizil miqdori;
- `GG` — yashil miqdori;
- `BB` — ko‘k miqdori.

Har bir juftlik `00` dan `FF` gacha bo‘ladi. `00` rang yo‘qligini, `FF` esa maksimal miqdorni bildiradi.

```text
#FF0000 — qizil
#00FF00 — yashil
#0000FF — ko‘k
#000000 — qora
#FFFFFF — oq
```

Qisqa HEX yozuvi ham mavjud:

```css
.short-white {
  color: #fff;
}

.short-black {
  color: #000;
}
```

### 2.3. RGB

RGB qizil, yashil va ko‘k kanallar orqali rang yaratadi. Har bir kanal `0` dan `255` gacha bo‘ladi.

```css
.blue {
  color: rgb(37, 99, 235);
}

.dark {
  background-color: rgb(15, 23, 42);
}
```

RGB rangini o‘zgartirishda uchta qiymatning vazifasini tushuning:

```css
/* Qizil ko‘proq, yashil va ko‘k kamroq */
.red {
  color: rgb(220, 38, 38);
}

/* Ko‘k ko‘proq, qizil va yashil kamroq */
.blue {
  color: rgb(37, 99, 235);
}
```

### 2.4. RGBA va alpha kanali

RGBA — RGB’ga alpha, ya’ni shaffoflik qo‘shilgan ko‘rinish. Alpha qiymati `0` dan `1` gacha bo‘ladi:

- `0` — butunlay shaffof;
- `0.5` — 50 foiz shaffof;
- `1` — to‘liq ko‘rinadigan.

```css
.transparent-blue {
  background-color: rgba(37, 99, 235, 0.15);
}

.glass-panel {
  background-color: rgba(15, 23, 42, 0.82);
}
```

Zamonaviy CSS’da slash yozuvi ham ishlatiladi:

```css
.modern-alpha {
  background-color: rgb(37 99 235 / 15%);
}
```

Alpha kanalini `opacity` bilan aralashtirib yubormang. `opacity` elementning ichidagi matn va barcha farzand elementlarni ham shaffof qiladi:

```css
/* Butun element, shu jumladan matn ham shaffof bo‘ladi */
.weak-card {
  opacity: 0.5;
}

/* Faqat fon shaffof bo‘ladi, matn to‘liq ko‘rinadi */
.better-card {
  background-color: rgb(37 99 235 / 15%);
}
```

### 2.5. HSL

HSL rangni inson uchun tushunarli uchta qismga ajratadi:

- **Hue** — rang tusi, `0`–`360` daraja;
- **Saturation** — rangning to‘yinganligi, foizda;
- **Lightness** — rangning yorqinligi, foizda.

```css
.hsl-blue {
  color: hsl(221, 83%, 53%);
}

.hsl-light-blue {
  background-color: hsl(214, 95%, 93%);
}

.hsl-dark-blue {
  background-color: hsl(222, 47%, 11%);
}
```

Bir rangning hover variantini HSL bilan topish qulay: hue va saturationni saqlab, lightnessni o‘zgartirasiz.

```css
.button {
  background-color: hsl(221, 83%, 53%);
}

.button:hover {
  background-color: hsl(221, 83%, 45%);
}
```

HSLA shaffoflikni ham qo‘llab-quvvatlaydi:

```css
.soft-purple {
  background-color: hsla(258, 90%, 66%, 0.18);
}
```

---

## 3. Ranglar xaritasi

Quyidagi SVG rang qiymatlarining turli ko‘rinishlarini taqqoslashga yordam beradi.

<svg viewBox="0 0 760 280" role="img" aria-label="CSS rang formatlari taqqoslanishi" style="width:100%;height:auto;background:#0f172a;border-radius:16px;padding:20px;box-sizing:border-box">
  <text x="30" y="34" fill="#f8fafc" font-size="22" font-weight="700" font-family="sans-serif">Bir xil ko‘k rangning turli yozilishi</text>
  <rect x="30" y="60" width="150" height="70" rx="12" fill="#2563eb"/>
  <text x="105" y="154" text-anchor="middle" fill="#bfdbfe" font-size="16" font-family="monospace">#2563EB</text>
  <rect x="210" y="60" width="150" height="70" rx="12" fill="rgb(37,99,235)"/>
  <text x="285" y="154" text-anchor="middle" fill="#bfdbfe" font-size="16" font-family="monospace">rgb(37,99,235)</text>
  <rect x="390" y="60" width="150" height="70" rx="12" fill="hsl(221,83%,53%)"/>
  <text x="465" y="154" text-anchor="middle" fill="#bfdbfe" font-size="16" font-family="monospace">hsl(221,83%,53%)</text>
  <rect x="570" y="60" width="150" height="70" rx="12" fill="rgb(37 99 235 / 55%)"/>
  <text x="645" y="154" text-anchor="middle" fill="#bfdbfe" font-size="16" font-family="monospace">alpha 55%</text>
  <text x="30" y="205" fill="#94a3b8" font-size="16" font-family="sans-serif">HEX — qisqa va mashhur</text>
  <text x="30" y="230" fill="#94a3b8" font-size="16" font-family="sans-serif">RGB — kanal qiymatlari</text>
  <text x="30" y="255" fill="#94a3b8" font-size="16" font-family="sans-serif">HSL — tus, to‘yinganlik, yorqinlik</text>
</svg>

---

## 4. CSS o‘zgaruvchilari bilan rang palitrasi

Bir loyihada bir xil ranglarni qayta-qayta yozmaslik uchun CSS custom property, ya’ni CSS o‘zgaruvchilaridan foydalaning.

```css
:root {
  --color-primary: #2563eb;
  --color-primary-dark: #1d4ed8;
  --color-accent: #06b6d4;
  --color-dark: #0f172a;
  --color-muted: #64748b;
  --color-surface: #ffffff;
  --color-page: #f8fafc;
}

body {
  background-color: var(--color-page);
  color: var(--color-dark);
}

.button {
  background-color: var(--color-primary);
  color: var(--color-surface);
}

.button:hover {
  background-color: var(--color-primary-dark);
}
```

O‘zgaruvchidan foydalanish sintaksisi:

```css
element {
  property: var(--variable-name);
}
```

Fallback qiymat berish ham mumkin:

```css
.title {
  color: var(--color-heading, #0f172a);
}
```

Agar `--color-heading` mavjud bo‘lmasa, `#0f172a` ishlatiladi.

---

## 5. Fon ranglari

### `background-color`

Elementning fon rangini belgilaydi.

```css
.page {
  background-color: #f8fafc;
}

.hero {
  background-color: #0f172a;
}

.card {
  background-color: white;
}
```

### Fon va matn kontrasti

To‘q fonda och matn, och fonda esa to‘q matn ishlating.

```css
.dark-section {
  background-color: #0f172a;
  color: #f8fafc;
}

.light-section {
  background-color: #f8fafc;
  color: #0f172a;
}
```

Och kulrang matnni oq fonda juda xira ishlatish o‘qishni qiyinlashtiradi. Muhim matnni yetarlicha kontrastli qiling.

### `background-image`

Fon sifatida rasm yoki gradient berish mumkin.

```css
.image-background {
  background-image: url("images/academy-background.jpg");
}
```

Rasm yo‘li CSS fayliga nisbatan hisoblanadi. Agar CSS `css/style.css` ichida, rasm esa `images/bg.jpg` ichida bo‘lsa:

```css
.hero {
  background-image: url("../images/bg.jpg");
}
```

### `background-size`

```css
.cover-background {
  background-size: cover;
}

.full-background {
  background-size: 100% 100%;
}

.original-background {
  background-size: auto;
}
```

`cover` rasmni elementni to‘liq qoplaydigan qilib kattalashtiradi. Ba’zi qismlar kesilishi mumkin, lekin bo‘sh joy qolmaydi.

### `background-position`

```css
.hero {
  background-position: center;
}

.hero-top {
  background-position: center top;
}

.hero-right {
  background-position: right center;
}
```

### `background-repeat`

```css
.no-repeat {
  background-repeat: no-repeat;
}

.repeat-x {
  background-repeat: repeat-x;
}
```

Ko‘pincha katta hero rasm uchun quyidagi qisqa yozuv ishlatiladi:

```css
.hero {
  background: url("hero.jpg") center / cover no-repeat;
}
```

---

## 6. Linear gradient

Gradient — bir rangdan boshqasiga silliq o‘tish. `linear-gradient()` to‘g‘ri chiziq bo‘ylab rang o‘zgartiradi.

```css
.blue-gradient {
  background: linear-gradient(#2563eb, #06b6d4);
}
```

Yo‘nalish berish:

```css
.to-right {
  background: linear-gradient(to right, #2563eb, #06b6d4);
}

.to-bottom-right {
  background: linear-gradient(to bottom right, #1d4ed8, #7c3aed);
}

.angle-gradient {
  background: linear-gradient(135deg, #2563eb, #7c3aed);
}
```

Daraja `0deg` yuqoriga, `90deg` o‘ngga, `180deg` pastga, `270deg` chapga yo‘nalishni anglatadi.

### Uch va undan ko‘p rang

```css
.academy-gradient {
  background: linear-gradient(
    135deg,
    #1d4ed8 0%,
    #2563eb 45%,
    #06b6d4 100%
  );
}
```

### Gradient overlay

Rasm ustiga qoramtir qatlam qo‘yib, matnni o‘qiladigan qilish mumkin.

```css
.hero {
  min-height: 360px;
  color: white;
  background:
    linear-gradient(rgb(15 23 42 / 75%), rgb(15 23 42 / 45%)),
    url("hero.jpg") center / cover no-repeat;
}
```

Bu yerda birinchi qatlam gradient, ikkinchi qatlam esa rasm. CSS’da birinchi yozilgan fon yuqorida turadi.

### Gradient chegarasi

```css
.gradient-border {
  padding: 2px;
  border-radius: 18px;
  background: linear-gradient(135deg, #06b6d4, #7c3aed);
}

.gradient-border__content {
  padding: 24px;
  border-radius: 16px;
  background: #0f172a;
  color: white;
}
```

---

## 7. Radial gradient

`radial-gradient()` ranglarni markazdan tashqariga qarab tarqatadi.

```css
.radial-blue {
  background: radial-gradient(circle, #60a5fa, #1d4ed8);
}
```

Markaz joylashuvini o‘zgartirish:

```css
.radial-corner {
  background: radial-gradient(
    circle at top right,
    #67e8f9,
    #1e3a8a 60%
  );
}
```

Radial gradient hero fonida yorug‘lik effekti, card’da glow yoki tugmada yumshoq rang o‘tishini yaratish uchun ishlatiladi.

```css
.glow-card {
  background:
    radial-gradient(circle at top left, rgb(37 99 235 / 35%), transparent 45%),
    #0f172a;
}
```

### Gradient ko‘rgazmali SVG

<svg viewBox="0 0 760 250" role="img" aria-label="Linear va radial gradient misoli" style="width:100%;height:auto;background:#f8fafc;border:1px solid #dbeafe;border-radius:16px;padding:18px;box-sizing:border-box">
  <defs>
    <linearGradient id="lesson-linear" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563eb"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
    <radialGradient id="lesson-radial" cx="35%" cy="30%" r="75%">
      <stop offset="0%" stop-color="#a78bfa"/>
      <stop offset="100%" stop-color="#4c1d95"/>
    </radialGradient>
  </defs>
  <rect x="30" y="35" width="330" height="130" rx="18" fill="url(#lesson-linear)"/>
  <rect x="400" y="35" width="330" height="130" rx="18" fill="url(#lesson-radial)"/>
  <text x="195" y="205" text-anchor="middle" fill="#1e3a8a" font-size="18" font-weight="700" font-family="sans-serif">linear-gradient()</text>
  <text x="565" y="205" text-anchor="middle" fill="#581c87" font-size="18" font-weight="700" font-family="sans-serif">radial-gradient()</text>
</svg>

---

## 8. Rang o‘tishlari va hover

Rang o‘zgarishini silliq qilish uchun `transition` ishlatiladi.

```css
.button {
  background-color: #2563eb;
  color: white;
  transition: background-color 180ms ease, transform 180ms ease;
}

.button:hover {
  background-color: #1d4ed8;
  transform: translateY(-2px);
}
```

`transition: all` ishlashi mumkin, lekin katta loyihalarda aniq xususiyatlarni yozish yaxshiroq:

```css
.card {
  transition: box-shadow 200ms ease, border-color 200ms ease;
}
```

Foydalanuvchi tugma yoki card ustiga sichqoncha olib kelganda rang o‘zgarishi sahifani jonli ko‘rsatadi. Lekin juda keskin ranglar yoki kuchli animatsiyalar foydalanuvchini chalg‘itishi mumkin.

---

## 9. Amaliy loyiha: rangli Academy hero section

Endi CSS ranglari va gradientlardan foydalanib, to‘liq hero section yaratamiz.

### `index.html`

```html
<!DOCTYPE html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Academy Hero</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main class="hero">
      <div class="hero__glow" aria-hidden="true"></div>

      <div class="hero__content">
        <p class="hero__eyebrow">CHAQIMCHIAI ACADEMY</p>
        <h1 class="hero__title">Kelajakni kod bilan yarating</h1>
        <p class="hero__text">
          HTML, CSS va dasturlashni sodda darslar, amaliy loyihalar va testlar
          orqali o‘rganing.
        </p>
        <div class="hero__actions">
          <a class="button button--primary" href="#courses">Kurslarni ko‘rish</a>
          <a class="button button--ghost" href="#about">Batafsil</a>
        </div>
      </div>
    </main>
  </body>
</html>
```

### `style.css`

```css
:root {
  --blue-600: #2563eb;
  --blue-700: #1d4ed8;
  --cyan-400: #22d3ee;
  --violet-500: #8b5cf6;
  --slate-950: #020617;
  --slate-200: #e2e8f0;
  --white: #ffffff;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: var(--slate-950);
}

.hero {
  position: relative;
  isolation: isolate;
  min-height: 560px;
  display: grid;
  place-items: center;
  overflow: hidden;
  padding: 48px 24px;
  color: var(--white);
  background:
    linear-gradient(135deg, rgb(15 23 42 / 96%), rgb(30 64 175 / 88%)),
    linear-gradient(45deg, var(--blue-700), var(--violet-500));
}

.hero::before,
.hero::after {
  position: absolute;
  z-index: -1;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  content: "";
  filter: blur(2px);
}

.hero::before {
  top: -140px;
  left: -80px;
  background: rgb(34 211 238 / 30%);
}

.hero::after {
  right: -100px;
  bottom: -170px;
  background: rgb(139 92 246 / 38%);
}

.hero__content {
  width: min(100%, 720px);
  text-align: center;
}

.hero__glow {
  position: absolute;
  inset: 15% 20%;
  z-index: -1;
  border-radius: 50%;
  background: radial-gradient(circle, rgb(37 99 235 / 30%), transparent 65%);
}

.hero__eyebrow {
  margin: 0 0 16px;
  color: var(--cyan-400);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.22em;
}

.hero__title {
  max-width: 680px;
  margin: 0 auto;
  font-size: clamp(36px, 7vw, 76px);
  line-height: 1.02;
}

.hero__text {
  max-width: 560px;
  margin: 24px auto 0;
  color: var(--slate-200);
  font-size: 18px;
  line-height: 1.7;
}

.hero__actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.button {
  display: inline-block;
  padding: 13px 20px;
  border: 1px solid transparent;
  border-radius: 12px;
  font-weight: 700;
  text-decoration: none;
  transition: background-color 180ms ease, border-color 180ms ease, transform 180ms ease;
}

.button:hover {
  transform: translateY(-2px);
}

.button--primary {
  background-color: var(--blue-600);
  color: var(--white);
}

.button--primary:hover {
  background-color: var(--blue-700);
}

.button--ghost {
  border-color: rgb(255 255 255 / 35%);
  color: var(--white);
  background-color: rgb(255 255 255 / 8%);
}

.button--ghost:hover {
  border-color: rgb(255 255 255 / 60%);
  background-color: rgb(255 255 255 / 15%);
}

@media (max-width: 520px) {
  .hero__actions,
  .button {
    width: 100%;
  }
}
```

### Loyihani yaxshilash

1. Hero’ga SVG logo qo‘shing.
2. Gradient ranglarini o‘zingizning uchta rangingiz bilan almashtiring.
3. Tugmalar hover holatlarini o‘zgartiring.
4. `background-position` yordamida fon joylashuvini sinab ko‘ring.
5. Telefon ekranida matn va tugmalarni tekshiring.

---

## 10. Ko‘p uchraydigan xatolar

### Rang qiymatida `#` tushib qolishi

```css
/* To‘g‘ri */
.title {
  color: #2563eb;
}

/* Noto‘g‘ri */
.title {
  color: 2563eb;
}
```

### RGB qiymatini 255 dan oshirish

```css
/* To‘g‘ri */
.blue {
  color: rgb(37, 99, 235);
}

/* Noto‘g‘ri fikr */
.blue {
  color: rgb(400, 99, 235);
}
```

### Gradientga yo‘nalish va ranglarni noto‘g‘ri berish

```css
/* To‘g‘ri */
.banner {
  background: linear-gradient(135deg, #2563eb, #06b6d4);
}
```

### Rasm yo‘lini noto‘g‘ri yozish

```css
/* style.css css papkasida, images esa loyiha ildizida bo‘lsa */
.hero {
  background-image: url("../images/hero.jpg");
}
```

### Matn kontrastini tekshirmaslik

Oq fonda och kulrang matn yoki to‘q fonda to‘q matn foydalanuvchiga noqulay. Har doim sahifani ko‘z bilan tekshiring va imkon bo‘lsa contrast checker’dan foydalaning.

### `opacity` bilan matnni ham xiralashtirish

Faqat fonni shaffof qilish kerak bo‘lsa, `rgba()` yoki slash alpha sintaksisidan foydalaning.

---

## 11. Mustahkamlash topshiriqlari

### Topshiriq 1: Rang palitrasi

Academy uchun 5 ta CSS o‘zgaruvchi yarating:

- asosiy ko‘k;
- hover ko‘k;
- accent cyan;
- sahifa foni;
- asosiy matn.

Keyin ularni body, sarlavha, card va tugmalarda ishlating.

### Topshiriq 2: Gradient card

`linear-gradient()` yordamida kurs card yarating. Card’da kurs nomi, tavsif va tugma bo‘lsin. Hover paytida card borderi rangini o‘zgartiring.

### Topshiriq 3: Radial glow

To‘q fonli section yarating va uning yuqori o‘ng burchagiga `radial-gradient()` orqali yorug‘lik effekti qo‘shing.

### Topshiriq 4: SVG ranglash

SVG ichida doira, to‘g‘ri to‘rtburchak va path yarating. Ularga class bering, ranglarini faqat CSS orqali boshqaring.

### Topshiriq 5: Fon rasmi

Hero section’ga rasm fon qo‘shing. Rasm ustida matn o‘qilishi uchun gradient overlay ishlating. `cover`, `center` va `no-repeat` xususiyatlarini qo‘llang.

---

## 12. Uyga vazifa: ranglar galereyasi

“CSS Color Gallery” nomli sahifa yarating. Unda:

- kamida 8 ta rangli card;
- har bir card’da rang nomi va HEX qiymati;
- 2 ta linear gradient card;
- 2 ta radial gradient card;
- bitta SVG ikonka;
- hover paytida rang yoki shadow o‘zgarishi;
- CSS o‘zgaruvchilaridan foydalanish

bo‘lsin.

Har bir rang cardi uchun matn o‘qilishi yaxshi bo‘lishini tekshiring. Kamida bitta rangni HEX, bittasini RGB, bittasini HSL va bittasini alpha qiymati bilan yozing.

---

## Dars xulosasi

Bugun CSS’da ranglarni nom, HEX, RGB, RGBA, HSL va HSLA ko‘rinishida yozishni o‘rgandik. Fon ranglari va rasmlarini boshqardik, linear va radial gradientlar yaratdik, shaffoflik hamda kontrastni tushundik. CSS o‘zgaruvchilari yordamida rang palitrasini markazlashtirdik va SVG bilan gradientlarni birgalikda ishlatdik.

Keyingi darsda shriftlar, matn o‘lchamlari, qator balandligi, tekislash va web tipografiya qoidalarini o‘rganamiz.
