# 1-Dars: CSS ga kirish — web sahifaga dizayn berish

## Dars maqsadi

Ushbu darsdan keyin siz:

- CSS nima ekanini va HTML bilan qanday ishlashini tushuntira olasiz;
- CSS qoidasining selektor, xususiyat va qiymatdan tuzilishini bilasiz;
- CSS’ni inline, internal va external usulda HTML’ga ulay olasiz;
- `tag`, `.class`, `#id` va guruh selectorlaridan foydalana olasiz;
- CSS izohlarini yozib, kodni tartibli saqlay olasiz;
- oddiy SVG ikonka va shakllarini HTML ichida ishlata olasiz;
- brauzer DevTools orqali CSS xatolarini topa olasiz;
- kichik, chiroyli va qayta ishlatiladigan profil card yaratishingiz mumkin bo‘ladi.

---

## 1. CSS nima?

**CSS** — *Cascading Style Sheets*, ya’ni “Kaskadlangan uslublar jadvali” degani. CSS HTML elementlarining ko‘rinishini boshqaradi.

HTML sahifaning **tuzilmasi** va mazmunini beradi:

```html
<h1>ChaqimchiAI Academy</h1>
<p>Dasturlashni bosqichma-bosqich o‘rganing.</p>
<button>Kurslarni ko‘rish</button>
```

CSS esa shu elementlarning:

- rangini;
- shriftini;
- o‘lchamini;
- oraliqlarini;
- chegarasini;
- joylashuvini;
- fonini;
- qurilmaga moslashishini

belgilaydi.

```css
h1 {
  color: #2563eb;
  font-size: 36px;
}

p {
  color: #475569;
  line-height: 1.7;
}

button {
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 12px 20px;
}
```

### HTML, CSS va JavaScript farqi

Ularni uyga o‘xshatib tasavvur qiling:

- **HTML** — uyning devori, xonalari va eshiklari;
- **CSS** — bo‘yoq, mebel, yorug‘lik va dizayn;
- **JavaScript** — eshikning ochilishi, tugmaning ishlashi va harakat.

HTML bo‘lmasa CSS bezaydigan element bo‘lmaydi. CSS bo‘lmasa HTML sahifa ishlashi mumkin, lekin u oddiy va bezaksiz ko‘rinadi. JavaScript esa sahifaga interaktivlik qo‘shadi.

### CSS qanday ishlaydi?

Brauzer HTML faylni o‘qiydi, CSS qoidalarini topadi va har bir qoida qaysi elementga mos kelishini aniqlaydi. Mos kelgan elementga stil qo‘llanadi.

```html
<h1 class="academy-title">ChaqimchiAI Academy</h1>
```

```css
.academy-title {
  color: #0f172a;
  font-size: 32px;
}
```

Bu yerda `.academy-title` selector bo‘lib, `class="academy-title"` bo‘lgan elementni topadi.

---

## 2. CSS qoidasining tuzilishi

CSS qoidasi quyidagi ko‘rinishga ega:

```css
selector {
  property: value;
}
```

Masalan:

```css
h1 {
  color: blue;
  font-size: 32px;
}
```

- `h1` — **selector**, ya’ni qaysi elementga stil berilishini ko‘rsatadi;
- `color` — **property**, ya’ni xususiyat;
- `blue` — **value**, ya’ni qiymat;
- `{ }` — CSS deklaratsiyalari joylashadigan blok;
- `:` — xususiyat va qiymatni ajratadi;
- `;` — deklaratsiya tugaganini bildiradi.

Bir selector ichida bir nechta xususiyat yozish mumkin:

```css
.notice {
  width: 320px;
  padding: 20px;
  color: #1e293b;
  background-color: #dbeafe;
  border: 1px solid #60a5fa;
  border-radius: 14px;
}
```

> Muhim: xususiyat nomida xato bo‘lsa yoki `:` yoki `;` tushib qolsa, brauzer o‘sha deklaratsiyani o‘tkazib yuborishi mumkin.

### CSS qoidasining SVG ko‘rgazmali rasmi

Quyidagi SVG CSS qoidasining qismlarini ko‘rsatadi. Bu oddiy rasm emas — u HTML ichida chizilgan vektorli grafika. Uni kattalashtirganda sifati buzilmaydi.

<svg viewBox="0 0 760 250" role="img" aria-label="CSS qoidasining tuzilishi" style="width:100%;height:auto;background:#0f172a;border-radius:16px;padding:18px;box-sizing:border-box">
  <text x="30" y="42" fill="#e2e8f0" font-size="24" font-family="monospace" font-weight="700">.card {</text>
  <text x="55" y="85" fill="#67e8f9" font-size="22" font-family="monospace">color</text>
  <text x="190" y="85" fill="#f8fafc" font-size="22" font-family="monospace">:</text>
  <text x="218" y="85" fill="#86efac" font-size="22" font-family="monospace">white</text>
  <text x="310" y="85" fill="#f8fafc" font-size="22" font-family="monospace">;</text>
  <text x="55" y="128" fill="#67e8f9" font-size="22" font-family="monospace">padding</text>
  <text x="190" y="128" fill="#f8fafc" font-size="22" font-family="monospace">:</text>
  <text x="218" y="128" fill="#fca5a5" font-size="22" font-family="monospace">20px</text>
  <text x="310" y="128" fill="#f8fafc" font-size="22" font-family="monospace">;</text>
  <text x="30" y="171" fill="#e2e8f0" font-size="24" font-family="monospace" font-weight="700">}</text>
  <line x1="380" y1="42" x2="500" y2="42" stroke="#60a5fa" stroke-width="2"/>
  <text x="515" y="49" fill="#bfdbfe" font-size="18" font-family="sans-serif">selector</text>
  <line x1="380" y1="85" x2="500" y2="85" stroke="#60a5fa" stroke-width="2"/>
  <text x="515" y="92" fill="#bfdbfe" font-size="18" font-family="sans-serif">property</text>
  <line x1="380" y1="128" x2="500" y2="128" stroke="#60a5fa" stroke-width="2"/>
  <text x="515" y="135" fill="#bfdbfe" font-size="18" font-family="sans-serif">value</text>
  <text x="30" y="225" fill="#94a3b8" font-size="16" font-family="sans-serif">Har bir deklaratsiya: property: value;</text>
</svg>

---

## 3. HTML bilan kichik tajriba

Quyidagi faylni `index.html` nomi bilan saqlang. Hozircha CSS’ni HTML ichiga yozamiz.

```html
<!DOCTYPE html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CSS tajriba</title>
  </head>
  <body>
    <h1>CSS bilan birinchi qadam</h1>
    <p>Bu sahifani CSS yordamida bezaymiz.</p>
    <button>Kirish</button>
  </body>
</html>
```

Bu sahifa brauzerda ishlaydi, ammo unda hali hech qanday maxsus dizayn yo‘q. Keyingi bo‘limlarda unga uch xil usulda CSS qo‘shamiz.

---

## 4. CSS’ni HTML’ga ulashning uch usuli

### 4.1. Inline CSS

Inline CSS elementning `style` atributi ichida yoziladi.

```html
<h1 style="color: #2563eb; font-size: 36px;">
  ChaqimchiAI Academy
</h1>

<p style="color: #475569;">
  Dasturlashni bosqichma-bosqich o‘rganing.
</p>

<button
  style="background: #2563eb; color: white; border: 0; padding: 12px 18px;"
>
  Boshlash
</button>
```

**Qachon ishlatish mumkin?** Bitta elementga tezkor va juda kichik o‘zgarish kiritishda.

**Kamchiligi:** Bir xil stilni boshqa elementlarga berish qiyin, HTML ichida kod ko‘payib ketadi. Katta loyihalarda inline CSS’dan asosiy usul sifatida foydalanilmaydi.

### 4.2. Internal CSS

Internal CSS `<head>` ichidagi `<style>` tegi orasida yoziladi.

```html
<!DOCTYPE html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <title>Internal CSS</title>

    <style>
      body {
        background-color: #f8fafc;
        font-family: Arial, sans-serif;
      }

      h1 {
        color: #1d4ed8;
      }

      p {
        color: #475569;
      }
    </style>
  </head>
  <body>
    <h1>Internal CSS</h1>
    <p>CSS shu HTML faylning ichida yozildi.</p>
  </body>
</html>
```

**Afzalligi:** Bitta HTML sahifaning barcha elementlarini tartibli boshqarish mumkin.

**Kamchiligi:** Bu stillar boshqa HTML fayllarga avtomatik ulanmaydi.

### 4.3. External CSS

Professional loyihalarda CSS odatda alohida faylda saqlanadi.

Papka tuzilishi:

```text
loyiha/
├── index.html
└── style.css
```

`index.html`:

```html
<!DOCTYPE html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>External CSS</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main class="page">
      <h1>External CSS</h1>
      <p>Stillar alohida style.css faylidan ulandi.</p>
    </main>
  </body>
</html>
```

`style.css`:

```css
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background-color: #f1f5f9;
  color: #0f172a;
  font-family: Arial, sans-serif;
}

.page {
  width: min(90%, 720px);
  margin: 80px auto;
  padding: 32px;
  background-color: white;
  border: 1px solid #dbeafe;
  border-radius: 18px;
  box-shadow: 0 12px 30px rgb(15 23 42 / 0.08);
}

h1 {
  margin-top: 0;
  color: #1d4ed8;
}

p {
  color: #475569;
  line-height: 1.7;
}
```

**External CSS’ning afzalliklari:**

1. HTML va dizayn alohida saqlanadi.
2. Bitta CSS faylini ko‘p sahifada ishlatish mumkin.
3. Kodni o‘qish va tuzatish osonlashadi.
4. Brauzer CSS faylini keshlashi sabab sahifa tezroq yuklanishi mumkin.

> Tavsiya: o‘quv mashqlarida uchala usulni sinab ko‘ring, haqiqiy loyihalarda esa asosan external CSS’dan foydalaning.

---

## 5. Selectorlar: CSS kimga ta’sir qiladi?

Selector CSS qaysi HTML elementga qo‘llanishini belgilaydi.

### 5.1. Tag selector

HTML tegining nomi yoziladi va shu turdagi barcha elementlarga stil beriladi.

```css
p {
  color: #475569;
  font-size: 18px;
}

button {
  cursor: pointer;
}
```

```html
<p>Birinchi paragraf.</p>
<p>Ikkinchi paragraf.</p>
```

Yuqoridagi ikkala `p` ham bir xil stil oladi.

### 5.2. Class selector

Class selector nuqta (`.`) bilan boshlanadi. Bir xil stilni ko‘p elementga berish uchun eng qulay usullardan biri.

```html
<p class="muted">Birinchi izoh</p>
<p class="muted">Ikkinchi izoh</p>
<button class="primary-button">Saqlash</button>
```

```css
.muted {
  color: #64748b;
}

.primary-button {
  border: 0;
  border-radius: 10px;
  padding: 10px 16px;
  background-color: #2563eb;
  color: white;
}
```

### 5.3. ID selector

ID selector `#` bilan boshlanadi. ID bir sahifada odatda faqat bitta elementga beriladi.

```html
<header id="site-header">
  <h1>Academy</h1>
</header>
```

```css
#site-header {
  padding: 24px;
  background-color: #0f172a;
  color: white;
}
```

Bir xil stil uchun ID’dan ko‘p foydalanish yaxshi amaliyot emas. Bunday vaziyatda class ishlating.

### 5.4. Universal selector

`*` barcha elementlarni tanlaydi.

```css
* {
  box-sizing: border-box;
}
```

Bu qoida element o‘lchamlarini hisoblashni boshqarish uchun juda ko‘p ishlatiladi.

### 5.5. Guruh selector

Bir nechta selectorning umumiy stilini vergul bilan yozish mumkin.

```css
h1,
h2,
h3 {
  color: #1e3a8a;
  font-family: Arial, sans-serif;
}
```

Bu yozuv uchta alohida qoida yozishdan qisqaroq va tartibliroq.

### 5.6. Ichki element selectorlari

Bo‘sh joy orqali bir element ichidagi boshqa elementni tanlash mumkin.

```css
.card p {
  color: #64748b;
}

.card a {
  color: #2563eb;
}
```

```html
<article class="card">
  <h2>Kurs</h2>
  <p>Kurs haqida ma’lumot.</p>
  <a href="#">Batafsil</a>
</article>
```

### Selectorlar bo‘yicha qisqa jadval

| Selector | Misol | Qaysi elementni tanlaydi? |
|---|---|---|
| Tag | `p` | Barcha `p` elementlarini |
| Class | `.card` | `class="card"` elementlarini |
| ID | `#header` | `id="header"` elementini |
| Universal | `*` | Barcha elementlarni |
| Guruh | `h1, h2` | `h1` va `h2` elementlarini |
| Ichki | `.card p` | `.card` ichidagi `p` ni |

---

## 6. CSS kaskadi va ustuvorlik

“Cascading” so‘zi bir nechta qoida bir elementga mos kelganda qaysi biri ustun bo‘lishini anglatadi.

```html
<p id="special" class="text">Salom</p>
```

```css
p {
  color: green;
}

.text {
  color: blue;
}

#special {
  color: red;
}
```

Bu holatda matn qizil bo‘ladi, chunki `id` selectorining ustuvorligi yuqoriroq.

Boshlang‘ich darajada quyidagi tartibni yodda tuting:

1. oddiy tag selector;
2. class va attribute selector;
3. ID selector;
4. inline style;
5. `!important` — faqat juda zarur vaziyatda.

```css
/* !important ni odat qilib olmang. */
.title {
  color: red !important;
}
```

`!important` keyinchalik kodni boshqarishni qiyinlashtiradi. Avval selectorlarni tartibli yozish va kaskadni tushunishga harakat qiling.

---

## 7. CSS izohlari

CSS izohi brauzer tomonidan bajarilmaydi. U kodni tushuntirish uchun yoziladi.

```css
/* Sahifaning asosiy foni */
body {
  background-color: #f8fafc;
}

/* Asosiy tugma */
.primary-button {
  background-color: #2563eb;
}
```

Bir nechta qatorni ham bitta izoh ichiga olish mumkin:

```css
/*
  Bu bo‘lim kurs cardlari uchun.
  Card fon, chegara va oraliqlarga ega.
*/
.course-card {
  padding: 20px;
  border-radius: 16px;
}
```

Izohlar kodni keyinroq o‘qiydigan o‘zingizga va jamoangizga yordam beradi. Lekin har bir qatorga keraksiz izoh yozish ham kodni shovqinli qiladi.

---

## 8. SVG nima va CSS bilan qanday ishlaydi?

**SVG** — *Scalable Vector Graphics*, ya’ni kattalashtirilganda sifati buzilmaydigan vektorli grafika. SVG ikonka, logo, diagramma va oddiy rasmlar uchun juda qulay.

SVG HTML ichida ishlatilishi mumkin:

```html
<svg
  width="120"
  height="120"
  viewBox="0 0 120 120"
  role="img"
  aria-label="Ko‘k doira ikonka"
>
  <circle cx="60" cy="60" r="48" fill="#dbeafe" />
  <circle cx="60" cy="60" r="32" fill="#2563eb" />
  <path
    d="M45 61l10 10 22-24"
    fill="none"
    stroke="white"
    stroke-width="7"
    stroke-linecap="round"
    stroke-linejoin="round"
  />
</svg>
```

Natija taxminan quyidagicha ko‘rinadi:

<svg viewBox="0 0 360 150" role="img" aria-label="SVG check ikonka namunasi" style="width:100%;max-width:360px;height:auto;background:#eff6ff;border:1px solid #bfdbfe;border-radius:16px;padding:20px;box-sizing:border-box">
  <circle cx="75" cy="75" r="48" fill="#dbeafe"/>
  <circle cx="75" cy="75" r="32" fill="#2563eb"/>
  <path d="M60 76l10 10 22-25" fill="none" stroke="white" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="145" y="69" fill="#1e3a8a" font-size="18" font-weight="700" font-family="sans-serif">SVG ikonka</text>
  <text x="145" y="94" fill="#475569" font-size="14" font-family="sans-serif">Sifat buzilmasdan</text>
  <text x="145" y="116" fill="#475569" font-size="14" font-family="sans-serif">kattalashtiriladi</text>
</svg>

### SVG’ga CSS class berish

SVG elementlariga ham class berib, ularni CSS orqali boshqarish mumkin.

```html
<svg class="academy-icon" viewBox="0 0 100 100" aria-hidden="true">
  <circle class="icon-bg" cx="50" cy="50" r="42" />
  <path class="icon-mark" d="M30 52l13 13 28-31" />
</svg>
```

```css
.academy-icon {
  width: 80px;
  height: 80px;
}

.icon-bg {
  fill: #dbeafe;
}

.icon-mark {
  fill: none;
  stroke: #2563eb;
  stroke-width: 8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.academy-icon:hover .icon-bg {
  fill: #bfdbfe;
}

.academy-icon:hover .icon-mark {
  stroke: #1d4ed8;
}
```

`viewBox` SVG ichki koordinatalarini belgilaydi. `width` va `height` esa ekrandagi o‘lchamni boshqaradi. SVG’ni responsive qilish uchun ko‘pincha `width: 100%` va `height: auto` ishlatiladi.

---

## 9. Amaliy loyiha: Academy profil card

Endi HTML va CSS’ni birlashtirib, to‘liq profil card yaratamiz.

### `index.html`

```html
<!DOCTYPE html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Academy Profile Card</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <main class="page-shell">
      <article class="profile-card">
        <div class="profile-icon" aria-hidden="true">
          <svg viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="46" class="avatar-bg" />
            <circle cx="50" cy="38" r="15" class="avatar-mark" />
            <path class="avatar-mark" d="M25 78c4-16 14-23 25-23s21 7 25 23" />
          </svg>
        </div>

        <p class="eyebrow">CHAQIMCHIAI ACADEMY</p>
        <h1 class="profile-name">Dasturlashni bugun boshlang</h1>
        <p class="profile-description">
          HTML, CSS va dasturlash asoslarini amaliy loyihalar orqali o‘rganing.
        </p>

        <a class="primary-button" href="#courses">Kurslarni ko‘rish</a>
      </article>
    </main>
  </body>
</html>
```

### `style.css`

```css
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #eff6ff;
  color: #0f172a;
  font-family: Arial, sans-serif;
}

.page-shell {
  width: min(100%, 480px);
}

.profile-card {
  padding: 36px 28px;
  text-align: center;
  background: white;
  border: 1px solid #bfdbfe;
  border-radius: 24px;
  box-shadow: 0 20px 50px rgb(30 64 175 / 0.14);
}

.profile-icon {
  width: 96px;
  height: 96px;
  margin: 0 auto 20px;
}

.profile-icon svg {
  display: block;
  width: 100%;
  height: 100%;
}

.avatar-bg {
  fill: #dbeafe;
  stroke: #60a5fa;
  stroke-width: 2;
}

.avatar-mark {
  fill: none;
  stroke: #2563eb;
  stroke-width: 7;
  stroke-linecap: round;
}

.avatar-mark:first-of-type {
  fill: #2563eb;
  stroke: none;
}

.eyebrow {
  margin: 0 0 10px;
  color: #2563eb;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.16em;
}

.profile-name {
  margin: 0;
  color: #0f172a;
  font-size: clamp(26px, 6vw, 38px);
  line-height: 1.1;
}

.profile-description {
  margin: 16px 0 24px;
  color: #475569;
  line-height: 1.7;
}

.primary-button {
  display: inline-block;
  padding: 12px 20px;
  border-radius: 10px;
  background: #2563eb;
  color: white;
  font-weight: 700;
  text-decoration: none;
  transition: background-color 180ms ease, transform 180ms ease;
}

.primary-button:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
}

@media (max-width: 420px) {
  .profile-card {
    padding: 28px 20px;
  }
}
```

### Kodni tekshirish

1. Bitta papka yarating.
2. Ichiga `index.html` va `style.css` fayllarini yarating.
3. Kodlarni tegishli fayllarga joylang.
4. `index.html` faylini brauzerda oching.
5. CSS o‘zgargandan keyin sahifani refresh qiling.
6. Telefon o‘lchamida ham card ko‘rinishini tekshiring.

---

## 10. Ko‘p uchraydigan xatolar

### CSS fayli ulanmayapti

HTML’dagi yo‘lni tekshiring:

```html
<link rel="stylesheet" href="style.css" />
```

Agar CSS `css/style.css` ichida bo‘lsa:

```html
<link rel="stylesheet" href="css/style.css" />
```

### Class nomi mos kelmayapti

```html
<p class="description">Matn</p>
```

```css
.discription {
  color: red;
}
```

Bu ishlamaydi, chunki HTML’da `description`, CSS’da esa `discription` yozilgan.

### Nuqta yoki hash tushib qolgan

```css
/* To‘g‘ri */
.card { }
#header { }

/* Noto‘g‘ri */
card { }
header { }
```

### CSS xususiyati noto‘g‘ri yozilgan

```css
.title {
  color: blue;
  font-size: 32px;
}
```

`font-size` o‘rniga `font size` yozilmaydi. CSS xususiyatlarida bo‘sh joy emas, tire ishlatiladi.

### Brauzer eski CSS’ni ko‘rsatmoqda

`Ctrl + R` yoki `Cmd + R` bilan refresh qiling. Zarur bo‘lsa hard refresh ishlating: `Ctrl + Shift + R` yoki `Cmd + Shift + R`.

### DevTools bilan tekshirish

1. Sahifada kerakli element ustiga o‘ng tugma bosing.
2. **Inspect** ni tanlang.
3. **Styles** panelida qaysi qoidalar ishlayotganini ko‘ring.
4. Ustidan chizilgan qoida ustuvorligi past yoki boshqa qoida bilan bosib ketilgan bo‘lishi mumkin.

---

## 11. Mustahkamlash topshiriqlari

### Topshiriq 1: Rangli xabar

`success`, `warning` va `error` classlariga ega uchta xabar yarating. Har biriga boshqa fon, matn rangi va chegara bering.

### Topshiriq 2: SVG ikonka

SVG yordamida doira ichida yulduz yoki yurak ikonka yarating. Uni `.icon` classi orqali `80px` o‘lchamga keltiring.

### Topshiriq 3: Kurs card

Kurs nomi, qisqa izoh, daraja va “Boshlash” tugmasidan iborat card yarating. Card’da:

- oq fon;
- yumaloq burchak;
- border;
- `padding`;
- hover paytida rang o‘zgarishi

bo‘lsin.

### Topshiriq 4: Uch xil ulash usuli

Bitta sahifada uchta paragraf yarating. Birinchisini inline, ikkinchisini internal, uchinchisini external CSS bilan bezang. Ularning farqini yozma ravishda tushuntiring.

---

## 12. Uyga vazifa: shaxsiy vizitka sahifasi

O‘zingiz haqingizda kichik vizitka sahifasi yarating. Unda quyidagilar bo‘lsin:

- ism va familiya;
- kasb yoki o‘rganayotgan yo‘nalish;
- qisqa bio;
- kamida uchta ko‘nikma;
- SVG avatar yoki ikonka;
- “Men bilan bog‘lanish” tugmasi;
- external `style.css` fayli;
- mobil qurilmaga mos ko‘rinish.

Talab: kamida 5 ta class selector, 1 ta ID selector, 1 ta guruh selector va 1 ta SVG element ishlating.

---

## Dars xulosasi

Bugun CSS’ning vazifasi, CSS qoidasi tuzilishi, uch xil ulash usuli va asosiy selectorlarni o‘rgandik. SVG yordamida sifatli vektorli ikonka qo‘shdik va uni CSS bilan boshqardik. Eng yaxshi amaliyot — HTML tuzilmasini, CSS dizaynini va keyinchalik JavaScript logikasini alohida saqlash.

Keyingi darsda ranglar, fonlar, gradientlar va rang qiymatlarini professional ishlatishni o‘rganamiz.
