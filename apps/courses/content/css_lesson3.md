# 3-Dars: Shriftlar va matn dizayni

## Dars maqsadi

Ushbu darsdan keyin siz:

- CSS’da shrift oilasi va shrift turini boshqara olasiz;
- `font-family`, `font-size`, `font-weight` va `font-style` xususiyatlarini ishlata olasiz;
- matn qator balandligi va harflar oralig‘ini sozlay olasiz;
- `text-align`, `text-decoration` va `text-transform` bilan ishlay olasiz;
- web-safe shriftlar va Google Fonts’dan foydalanishni bilasiz;
- sarlavha, paragraf, label va tugma uchun tipografik ierarxiya yarata olasiz;
- `rem`, `em`, `vw` va `clamp()` yordamida responsive matn yozasiz;
- SVG ichidagi matnni CSS orqali bezay olasiz;
- o‘qilishi qulay landing section yarata olasiz.

---

## 1. Tipografiya nima?

**Tipografiya** — matnni o‘qish qulay, chiroyli va ma’noli ko‘rsatish san’ati. Web sahifada foydalanuvchi avvalo matnni o‘qiydi, shuning uchun rang bilan birga shrift ham juda muhim.

Yaxshi tipografiya quyidagilarni ta’minlaydi:

- sarlavha va oddiy matn o‘rtasidagi farq;
- ma’lumotlarning ustuvorligi;
- qatorlarni oson kuzatish;
- mobil ekranda ham o‘qilishi;
- brendning o‘ziga xos ko‘rinishi.

```css
body {
  color: #0f172a;
  font-family: Arial, sans-serif;
}

h1 {
  font-size: 48px;
  font-weight: 800;
  line-height: 1.05;
}

p {
  max-width: 60ch;
  color: #475569;
  font-size: 18px;
  line-height: 1.7;
}
```

---

## 2. `font-family`

`font-family` matn qaysi shrift oilasida chiqishini belgilaydi.

```css
body {
  font-family: Arial, sans-serif;
}

.code-text {
  font-family: "Courier New", monospace;
}

.serif-title {
  font-family: Georgia, serif;
}
```

### Fallback shriftlar

Brauzer birinchi shriftni topa olmasa, keyingi shriftga o‘tadi:

```css
body {
  font-family: "Inter", Arial, sans-serif;
}
```

Bu yerda:

1. brauzer `Inter`ni qidiradi;
2. topilmasa `Arial`ni ishlatadi;
3. u ham mavjud bo‘lmasa, tizimdagi sans-serif shriftni tanlaydi.

Shrift nomida bo‘sh joy bo‘lsa, uni qo‘shtirnoq ichida yozing:

```css
.heading {
  font-family: "Trebuchet MS", Arial, sans-serif;
}
```

### Shrift oilalari

| Oila | Ko‘rinishi | Misollar |
|---|---|---|
| `serif` | Harf uchlarida kichik bezaklar bor | Georgia, Times New Roman |
| `sans-serif` | Toza va zamonaviy | Arial, Inter, Roboto |
| `monospace` | Har bir belgi eni teng | Consolas, Courier New |
| `cursive` | Qo‘l yozuviga o‘xshash | Comic Sans MS |
| `fantasy` | Dekorativ | Maxsus display shriftlar |

O‘quv platformalari va dasturlash saytlarida ko‘pincha sans-serif shriftlar, kod uchun esa monospace shriftlar ishlatiladi.

---

## 3. Google Fonts ulash

Google Fonts — bepul web shriftlar kutubxonasi. Shriftni HTML’dagi `<head>` ichiga ulash mumkin.

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
    rel="stylesheet"
  />

  <link rel="stylesheet" href="style.css" />
</head>
```

Keyin CSS’da foydalaning:

```css
body {
  font-family: "Inter", Arial, sans-serif;
}
```

Bir nechta oila ulash:

```html
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap"
  rel="stylesheet"
/> 
```

```css
body {
  font-family: "Inter", sans-serif;
}

code,
.code {
  font-family: "JetBrains Mono", monospace;
}
```

> Ishlab chiqarish loyihasida tashqi shrift serveri ishlamagan holat uchun doim fallback shrift yozing.

---

## 4. `font-size` va o‘lchov birliklari

`font-size` matn o‘lchamini belgilaydi.

```css
h1 {
  font-size: 48px;
}

p {
  font-size: 18px;
}
```

### `px`

`px` aniq o‘lcham beradi. U kichik komponentlar va borderlar uchun qulay.

```css
.badge {
  font-size: 12px;
}
```

### `rem`

`rem` ildiz element, odatda `html`, o‘lchamiga bog‘liq. Brauzerning odatiy o‘lchami ko‘pincha `16px` bo‘ladi.

```css
html {
  font-size: 16px;
}

h1 {
  font-size: 3rem; /* 48px */
}

p {
  font-size: 1.125rem; /* 18px */
}
```

`rem` accessibility uchun qulay, chunki foydalanuvchi brauzer shriftini kattalashtirganda sahifa yaxshiroq moslashadi.

### `em`

`em` ota elementning shrift o‘lchamiga bog‘liq.

```css
.card {
  font-size: 20px;
}

.card h2 {
  font-size: 1.5em; /* 30px */
}
```

Ichma-ich elementlarda `em` o‘lchami kutilmaganda kattalashishi mumkin. Shu sababli katta loyihalarda umumiy tipografiya uchun `rem` qulayroq.

### `vw`

`vw` viewport kengligining foiziga teng.

```css
.fluid-title {
  font-size: 6vw;
}
```

Bu usul matnni ekranga moslashtiradi, ammo juda kichik yoki juda katta bo‘lib ketmasligi uchun `clamp()` bilan ishlatish yaxshiroq.

### `clamp()`

`clamp(minimum, preferred, maximum)` matnning eng kichik, afzal va eng katta chegarasini belgilaydi.

```css
.hero-title {
  font-size: clamp(2rem, 6vw, 5rem);
}
```

Bu sarlavha:

- kichik ekranda `2rem`dan kichik bo‘lmaydi;
- viewportga qarab `6vw` bilan o‘zgaradi;
- katta ekranda `5rem`dan oshmaydi.

---

## 5. `font-weight`, `font-style` va `font-variant`

### `font-weight`

Matn qalinligini belgilaydi.

```css
.regular {
  font-weight: 400;
}

.medium {
  font-weight: 500;
}

.semibold {
  font-weight: 600;
}

.bold {
  font-weight: 700;
}

.extra-bold {
  font-weight: 800;
}
```

Agar Google Font’da faqat `400` va `700` yuklangan bo‘lsa, `600` uchun brauzer o‘ziga yaqin variantni taqlid qilishi mumkin. Ishlatadigan qalinliklaringizni oldindan yuklang.

### `font-style`

```css
.normal-text {
  font-style: normal;
}

.italic-text {
  font-style: italic;
}
```

### `font-variant`

```css
.small-caps {
  font-variant: small-caps;
}
```

### Shorthand `font`

Bir nechta shrift xususiyatini bitta qatorda yozish mumkin:

```css
.summary {
  font: italic 600 18px/1.7 "Inter", Arial, sans-serif;
}
```

Tartibi:

```text
font-style font-weight font-size/line-height font-family
```

Boshlang‘ich bosqichda xatoni kamaytirish uchun xususiyatlarni alohida yozish ham yaxshi.

---

## 6. Qator balandligi va matn oralig‘i

### `line-height`

`line-height` qatorlar orasidagi vertikal masofani belgilaydi.

```css
body {
  line-height: 1.5;
}

.article-text {
  line-height: 1.8;
}

.hero-title {
  line-height: 1.05;
}
```

Paragraflar uchun `1.5`–`1.8`, katta sarlavhalar uchun `1.0`–`1.2` atrofidagi qiymatlar ko‘p ishlatiladi.

Unitless qiymat yozish foydali:

```css
body {
  line-height: 1.5;
}
```

Shunda line-height elementning o‘z `font-size`iga mos ravishda hisoblanadi.

### `letter-spacing`

Harflar orasidagi masofani boshqaradi.

```css
.eyebrow {
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.tight-title {
  letter-spacing: -0.03em;
}
```

Katta sarlavhada ozgina manfiy spacing, kichik uppercase label’da esa musbat spacing ishlatilishi mumkin.

### `word-spacing`

So‘zlar orasidagi masofani boshqaradi.

```css
.wide-words {
  word-spacing: 0.3em;
}
```

Bu xususiyatni ehtiyotkorlik bilan ishlating; juda katta qiymat matn oqimini buzadi.

### Tipografiya SVG ko‘rgazmasi

<svg viewBox="0 0 760 280" role="img" aria-label="Tipografiya o'lchamlari va qator balandligi" style="width:100%;height:auto;background:#0f172a;border-radius:16px;padding:20px;box-sizing:border-box">
  <text x="30" y="40" fill="#f8fafc" font-size="28" font-weight="800" font-family="sans-serif">Sarlavha</text>
  <text x="30" y="72" fill="#67e8f9" font-size="15" font-family="monospace">font-size: 28px; font-weight: 800;</text>
  <line x1="30" y1="96" x2="710" y2="96" stroke="#334155"/>
  <text x="30" y="130" fill="#e2e8f0" font-size="18" font-family="sans-serif">Paragraf matni qatorlar orasida yetarli masofa bilan o‘qiladi.</text>
  <text x="30" y="164" fill="#e2e8f0" font-size="18" font-family="sans-serif">Qator balandligi matnni kuzatishni osonlashtiradi.</text>
  <text x="30" y="205" fill="#67e8f1" font-size="15" font-family="monospace">font-size: 18px; line-height: 1.8;</text>
  <text x="30" y="250" fill="#94a3b8" font-size="15" font-family="sans-serif">O‘lcham + qalinlik + qator balandligi = o‘qilishi qulay matn</text>
</svg>

---

## 7. Matnni tekislash

### `text-align`

```css
.left {
  text-align: left;
}

.center {
  text-align: center;
}

.right {
  text-align: right;
}

.justify {
  text-align: justify;
}
```

Landing page hero matni ko‘pincha markazda, maqola matni esa chap tomonda bo‘ladi. `justify` uzun matnda chetlarni tekislaydi, lekin so‘zlar orasida katta bo‘shliq paydo bo‘lishi mumkin.

### `text-align-last`

```css
.article-intro {
  text-align: justify;
  text-align-last: left;
}
```

### `vertical-align`

`vertical-align` inline yoki table elementlari bilan ishlatiladi.

```css
.icon-text img {
  vertical-align: middle;
}
```

Flex yoki Grid layout’da vertikal joylashuv uchun `align-items` ishlatiladi; `vertical-align` ularning o‘rnini bosmaydi.

---

## 8. Matn bezaklari va shakli

### `text-decoration`

```css
.link {
  text-decoration: underline;
  text-decoration-color: #2563eb;
  text-decoration-thickness: 2px;
  text-underline-offset: 4px;
}

.clean-link {
  text-decoration: none;
}

.deleted-price {
  text-decoration: line-through;
}
```

Link’larni butunlay bezaksiz qilsangiz, ularni rang, hover yoki boshqa vizual belgi bilan link ekanini ko‘rsating.

### `text-transform`

```css
.uppercase {
  text-transform: uppercase;
}

.lowercase {
  text-transform: lowercase;
}

.capitalize {
  text-transform: capitalize;
}
```

```html
<p class="eyebrow">web dasturlash kursi</p>
```

```css
.eyebrow {
  color: #2563eb;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
```

### `text-overflow` va uzun matn

Bir qatorli matnni ellipsis bilan qisqartirish:

```css
.single-line {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

Bir nechta qatorni cheklash uchun zamonaviy usul:

```css
.description {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}
```

### `overflow-wrap`

Uzun URL yoki bitta so‘z container’dan chiqib ketmasligi uchun:

```css
article {
  overflow-wrap: anywhere;
}
```

---

## 9. Matn kengligi va o‘qish qulayligi

Juda uzun qatorni o‘qish qiyin. Matn container’ini cheklang.

```css
.article {
  width: min(100%, 720px);
  margin: 0 auto;
}

.article p {
  max-width: 65ch;
}
```

`ch` belgilar kengligiga asoslangan birlik. Paragraf uchun `45ch`–`75ch` oralig‘i ko‘pincha qulay bo‘ladi.

```css
.hero-copy {
  max-width: 52ch;
  margin-inline: auto;
}
```

Sarlavha uchun ham max-width belgilang:

```css
.hero-title {
  max-width: 12ch;
  margin-inline: auto;
}
```

Bu katta sarlavhaning juda uzun bitta qatorga cho‘zilib ketishini oldini oladi.

---

## 10. Amaliy loyiha: Academy tipografik hero

### `index.html`

```html
<!DOCTYPE html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="style.css" />
    <title>Academy Typography</title>
  </head>
  <body>
    <main class="hero">
      <div class="hero__mark" aria-hidden="true">
        <svg viewBox="0 0 120 120">
          <circle class="mark-ring" cx="60" cy="60" r="48" />
          <path class="mark-path" d="M35 61l16 16 34-38" />
        </svg>
      </div>

      <p class="eyebrow">CHAQIMCHIAI ACADEMY</p>
      <h1 class="hero__title">Kod yozing. Fikr yarating. Kelajakni quring.</h1>
      <p class="hero__description">
        Dasturlashni sodda tushuntirishlar, amaliy loyihalar va o‘yinli testlar
        orqali o‘rganing.
      </p>
      <a class="hero__button" href="#start">O‘rganishni boshlash</a>
    </main>
  </body>
</html>
```

### `style.css`

```css
:root {
  --blue: #2563eb;
  --blue-dark: #1e3a8a;
  --cyan: #22d3ee;
  --ink: #0f172a;
  --muted: #475569;
  --surface: #ffffff;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #eff6ff;
  color: var(--ink);
  font-family: "Inter", Arial, sans-serif;
}

.hero {
  width: min(100% - 32px, 960px);
  min-height: 620px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 16px auto;
  padding: 56px 24px;
  overflow: hidden;
  border: 1px solid #bfdbfe;
  border-radius: 28px;
  text-align: center;
  background:
    radial-gradient(circle at 10% 10%, rgb(34 211 238 / 25%), transparent 28%),
    linear-gradient(135deg, var(--blue-dark), var(--blue));
  color: var(--surface);
}

.hero__mark {
  width: 92px;
  height: 92px;
  margin-bottom: 24px;
}

.hero__mark svg {
  width: 100%;
  height: 100%;
}

.mark-ring {
  fill: rgb(255 255 255 / 12%);
  stroke: rgb(255 255 255 / 60%);
  stroke-width: 2;
}

.mark-path {
  fill: none;
  stroke: var(--cyan);
  stroke-width: 8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.eyebrow {
  margin: 0 0 18px;
  color: #a5f3fc;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.2em;
}

.hero__title {
  max-width: 13ch;
  margin: 0;
  font-size: clamp(2.4rem, 7vw, 5.5rem);
  font-weight: 800;
  letter-spacing: -0.045em;
  line-height: 1.02;
}

.hero__description {
  max-width: 55ch;
  margin: 24px 0 0;
  color: #dbeafe;
  font-size: clamp(1rem, 2vw, 1.25rem);
  line-height: 1.75;
}

.hero__button {
  margin-top: 32px;
  padding: 14px 22px;
  border-radius: 12px;
  background: var(--surface);
  color: var(--blue-dark);
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 180ms ease, box-shadow 180ms ease;
}

.hero__button:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 26px rgb(2 6 23 / 25%);
}

@media (max-width: 520px) {
  .hero {
    min-height: 560px;
    width: min(100% - 20px, 960px);
    padding-inline: 18px;
  }
}
```

---

## 11. Ko‘p uchraydigan xatolar

### Shrift nomini noto‘g‘ri yozish

```css
/* To‘g‘ri */
body {
  font-family: "Inter", Arial, sans-serif;
}

/* Bo‘sh joyli nom qo‘shtirnoqsiz yozilgan */
.wrong {
  font-family: Inter Tight, sans-serif;
}
```

### `line-height`ni juda kichik qilish

```css
/* Paragraf uchun juda siqilgan */
.bad-text {
  line-height: 0.8;
}

/* O‘qilishi qulayroq */
.good-text {
  line-height: 1.7;
}
```

### Sarlavhani haddan tashqari katta qilish

Desktop’da chiroyli ko‘ringan `80px` sarlavha telefonda ekrandan chiqib ketishi mumkin. `clamp()` va `max-width` ishlating.

### `text-align: center`ni hamma joyda ishlatish

Markaziy hero uchun qulay bo‘lsa-da, uzun maqola va dars matni chap tomonda o‘qilishi osonroq.

### Matn rangini juda xira qilish

```css
/* O‘qilishi qiyin */
.bad-muted {
  color: #cbd5e1;
  background: white;
}
```

Muted matn ham fon bilan yetarli kontrastga ega bo‘lishi kerak.

### Google Fonts og‘irligini ulab, CSS’da ishlatmaslik

Faqat kerakli `400`, `600`, `700` kabi og‘irliklarni ulang. Keraksiz ko‘p font variantlari sahifa yuklanishini og‘irlashtiradi.

---

## 12. Mustahkamlash topshiriqlari

### Topshiriq 1: Tipografik scale

Quyidagi elementlar uchun CSS o‘lchamlar jadvalini yarating:

- `h1` — hero sarlavha;
- `h2` — bo‘lim sarlavhasi;
- `h3` — card sarlavhasi;
- `p` — asosiy paragraf;
- `.caption` — kichik izoh.

Har biriga `font-size`, `font-weight` va `line-height` belgilang.

### Topshiriq 2: Shrift taqqoslash

Bir sahifada `serif`, `sans-serif` va `monospace` shriftlarida uchta card yarating. Qaysi vazifa uchun qaysi shrift mosligini yozing.

### Topshiriq 3: Responsive sarlavha

`clamp()` yordamida telefonda 32px dan kichik bo‘lmaydigan va katta ekranda 80px dan oshmaydigan sarlavha yarating.

### Topshiriq 4: SVG label

SVG ichida ikonka va uning yonida matn yarating. Matnni CSS class orqali rang, o‘lcham va qalinlik bilan boshqaring.

### Topshiriq 5: Maqola o‘qilishi

720px kenglikdagi maqola container yarating. Paragraflarga `max-width: 65ch`, `font-size: 18px` va `line-height: 1.8` bering.

---

## 13. Uyga vazifa: shaxsiy landing hero

O‘zingiz tanlagan mavzu uchun landing page hero yarating. Masalan: portfolio, kurs, mobil ilova yoki Telegram bot.

Talablar:

- Google Fonts yoki fallback shriftlar;
- responsive `clamp()` sarlavha;
- eyebrow label;
- 2–3 qatorli izoh;
- kamida bitta SVG ikonka;
- primary va secondary tugma;
- `letter-spacing`, `line-height` va `font-weight` ishlatilishi;
- mobil ekranda matn sig‘ishi;
- link va tugmalarda hover holati.

---

## Dars xulosasi

Bugun CSS tipografiyasining asoslarini o‘rgandik: shrift oilalari, Google Fonts, o‘lchov birliklari, qalinlik, qator balandligi, harflar oralig‘i, matn tekislash va bezaklar. `rem`, `ch` va `clamp()` yordamida turli ekranlarga mos matn yaratdik. SVG ichidagi matnni ham CSS orqali boshqarib, to‘liq Academy hero section qurdik.

Keyingi darsda CSS box model — `width`, `height`, `margin`, `padding`, `border` va `box-sizing` mavzularini chuqur o‘rganamiz.
