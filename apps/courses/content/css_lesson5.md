# 5-Dars: Selectorlar, pseudo-class va pseudo-elementlar

## Dars maqsadi

Ushbu darsdan keyin siz:

- CSS selectorlarining asosiy turlarini ishlata olasiz;
- class va ID selectorlaridan to‘g‘ri foydalanasiz;
- ichki, farzand va qo‘shni elementlarni tanlay olasiz;
- attribute selectorlar yordamida elementlarni filtrlaysiz;
- `:hover`, `:focus`, `:active`, `:checked` kabi pseudo-classlarni ishlatasiz;
- `::before` va `::after` orqali dekorativ elementlar yaratasiz;
- selector ustuvorligi va specificity’ni tushunasiz;
- amaliy navigation va interactive card yarata olasiz.

---

## 1. Selector nima?

Selector CSS qaysi HTML elementga stil berilishini ko‘rsatadi.

```css
p {
  color: #475569;
}
```

Bu qoida barcha `<p>` elementlarini tanlaydi. CSS’da selectorlar qanchalik aniq yozilsa, kerakli elementni boshqarish shunchalik oson bo‘ladi.

---

## 2. Asosiy selectorlar

### Universal selector: `*`

`*` barcha elementlarni tanlaydi.

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

Bu reset qoidasi Box Model darsida ko‘rganimizdek, o‘lchamlarni oldindan hisoblashni osonlashtiradi.

### Tag selector

```css
h1 {
  color: #0f172a;
}

button {
  cursor: pointer;
}
```

Tag selector barcha bir xil teglar uchun ishlaydi. Umumiy qoidalar uchun qulay, lekin alohida card yoki tugmaga turlicha stil berishda class yaxshiroq.

### Class selector

Class nuqta bilan yoziladi.

```html
<p class="muted">Qo‘shimcha ma’lumot</p>
<button class="primary-button">Boshlash</button>
```

```css
.muted {
  color: #64748b;
}

.primary-button {
  padding: 12px 18px;
  border: 0;
  border-radius: 10px;
  background: #2563eb;
  color: white;
}
```

Bir class’ni bir nechta elementda qayta ishlatish mumkin. Bu eng ko‘p ishlatiladigan selector turidir.

### ID selector

ID hash bilan yoziladi.

```html
<header id="site-header">Academy</header>
```

```css
#site-header {
  padding: 20px;
  background: #0f172a;
  color: white;
}
```

ID bir sahifada odatda bitta noyob element uchun ishlatiladi. Bir xil komponentlar uchun ID emas, class tanlang.

### Guruh selector

```css
h1,
h2,
h3 {
  color: #1e3a8a;
  line-height: 1.15;
}
```

Bir nechta selectorning umumiy stilini vergul orqali birlashtirish mumkin.

---

## 3. Bir nechta class va selector kombinatsiyasi

Elementga bir nechta class berish mumkin:

```html
<button class="button button-primary button-large">
  Kursni boshlash
</button>
```

```css
.button {
  border: 0;
  border-radius: 10px;
  font-weight: 700;
}

.button-primary {
  background: #2563eb;
  color: white;
}

.button-large {
  padding: 14px 24px;
}
```

Bu yondashuv umumiy qoidalarni `.button`ga, variantlarni esa alohida classlarga ajratadi.

Element va classni birga yozish:

```css
button.primary-button {
  background: #2563eb;
}
```

Bu faqat `button` tegidagi `primary-button` classga ta’sir qiladi. `a class="primary-button"` bunday qoidaga mos kelmaydi.

---

## 4. Ichki va farzand selectorlar

### Descendant selector

Bo‘sh joy orqali bir element ichidagi barcha mos elementlar tanlanadi.

```html
<article class="card">
  <h2>Kurs nomi</h2>
  <div class="card-body">
    <p>Kurs haqida ma’lumot.</p>
  </div>
</article>
```

```css
.card p {
  color: #64748b;
}
```

`.card` ichidagi istalgan chuqurlikdagi `p` tanlanadi.

### Child selector: `>`

`>` faqat bevosita farzandni tanlaydi.

```css
.menu > li {
  list-style: none;
}
```

```html
<ul class="menu">
  <li>Bosh sahifa</li>
  <li>
    Kurslar
    <ul>
      <li>HTML</li>
    </ul>
  </li>
</ul>
```

Yuqoridagi qoida faqat tashqi `ul`ning bevosita `li` elementlariga ishlaydi. Ichki `li`ga ishlamaydi.

### Keyingi sibling: `+`

`+` bir elementdan keyin darhol kelgan elementni tanlaydi.

```css
h2 + p {
  margin-top: 0;
  color: #475569;
}
```

### General sibling: `~`

`~` bir xil ota ichida undan keyin kelgan barcha mos siblinglarni tanlaydi.

```css
input:checked ~ .details {
  display: block;
}
```

---

## 5. Attribute selectorlar

Attribute selector HTML atributiga qarab element tanlaydi.

```css
input[type="email"] {
  border-color: #2563eb;
}

input[required] {
  border-left: 3px solid #ef4444;
}

a[target="_blank"] {
  color: #7c3aed;
}
```

### Natija

<div style="display:grid;gap:10px;max-width:420px;margin:16px 0">
  <input type="email" value="email@example.com" readonly style="padding:11px 14px;border:2px solid #2563eb;border-radius:10px;color:#0f172a;background:white" />
  <input type="text" value="Majburiy maydon" readonly style="padding:11px 14px;border:1px solid #cbd5e1;border-left:3px solid #ef4444;border-radius:10px;color:#0f172a;background:white" />
</div>

Ko‘p ishlatiladigan attribute operatorlari:

```css
/* Atribut mavjud */
[disabled] { opacity: 0.5; }

/* Qiymat aynan teng */
[type="submit"] { cursor: pointer; }

/* Qiymat shu bilan boshlanadi */
[href^="https"] { color: green; }

/* Qiymat shu bilan tugaydi */
[href$=".pdf"] { color: red; }

/* Qiymat ichida shu qism bor */
[class*="card"] { border-radius: 16px; }
```

---

## 6. Pseudo-class nima?

Pseudo-class elementning maxsus holatini tanlaydi. U bitta `:` bilan yoziladi.

### `:hover`

Foydalanuvchi sichqonchani element ustiga olib kelganda ishlaydi.

```css
.link {
  color: #2563eb;
  text-decoration: none;
}

.link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}
```

### `:focus`

Input yoki button klaviatura/sichqoncha orqali faol bo‘lganda ishlaydi.

```css
input:focus {
  border-color: #2563eb;
  outline: 3px solid rgb(37 99 235 / 18%);
}
```

### `:focus-visible`

Odatda klaviatura orqali kelgan focus holatini ko‘rsatish uchun qulay.

```css
button:focus-visible {
  outline: 3px solid #22d3ee;
  outline-offset: 3px;
}
```

### `:active`

Element bosib turilgan paytda ishlaydi.

```css
.button:active {
  transform: scale(0.97);
}
```

### `:visited`

Foydalanuvchi tashrif buyurgan linkni tanlaydi.

```css
a:visited {
  color: #7c3aed;
}
```

Maxfiylik sabab `:visited` uchun barcha CSS xususiyatlari ishlamaydi. Uni rang va oddiy bezaklar bilan cheklang.

### `:disabled` va `:enabled`

```css
button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

button:enabled:hover {
  background: #1d4ed8;
}
```

### `:checked`

Checkbox yoki radio tanlanganda ishlaydi.

```html
<label class="check-row">
  <input type="checkbox" />
  <span>Yangiliklarga obuna bo‘lish</span>
</label>
```

```css
.check-row:has(input:checked) {
  color: #166534;
  background: #dcfce7;
}
```

`:has()` zamonaviy brauzerlarda ota elementni ichki holatga qarab tanlash imkonini beradi.

---

## 7. Structural pseudo-classlar

### `:first-child`, `:last-child`

```css
.lesson-list li:first-child {
  border-top: 0;
}

.lesson-list li:last-child {
  border-bottom: 0;
}
```

### `:nth-child()`

```css
.lesson-list li:nth-child(2) {
  background: #eff6ff;
}

.lesson-list li:nth-child(even) {
  background: #f8fafc;
}

.lesson-list li:nth-child(odd) {
  background: white;
}
```

`nth-child(3n)` har uchinchi elementni tanlaydi:

```css
.grid-card:nth-child(3n) {
  border-color: #06b6d4;
}
```

### Natija

<div style="max-width:420px;margin:16px 0;border:1px solid #dbeafe;border-radius:12px;overflow:hidden">
  <div style="padding:13px 16px;background:#f8fafc;border-bottom:1px solid #e2e8f0;color:#0f172a">1. HTML asoslari</div>
  <div style="padding:13px 16px;background:#eff6ff;border-bottom:1px solid #e2e8f0;color:#1d4ed8;font-weight:700">2. CSS ranglari</div>
  <div style="padding:13px 16px;background:white;border-bottom:1px solid #e2e8f0;color:#0f172a">3. Box Model</div>
  <div style="padding:13px 16px;background:#f8fafc;color:#0f172a">4. Selectorlar</div>
</div>

---

## 8. Pseudo-element nima?

Pseudo-element elementning ma’lum bir qismini yoki virtual qismini tanlaydi. U ikki nuqta bilan yoziladi: `::before`, `::after`, `::first-letter`, `::selection`.

### `::before` va `::after`

```css
.section-title::before {
  content: "";
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 8px;
  border-radius: 50%;
  background: #2563eb;
}
```

`content` xususiyati `::before` va `::after` uchun majburiy. Bo‘sh dekorativ element bo‘lsa ham `content: ""` yoziladi.

```css
.external-link::after {
  content: " ↗";
  color: #2563eb;
}
```

### Natija

<div style="margin:16px 0;color:#0f172a;font-size:20px;font-weight:700"><span style="display:inline-block;width:8px;height:8px;margin-right:8px;border-radius:50%;background:#2563eb;vertical-align:middle"></span>CSS darslari</div>

Pseudo-elementlar DOM’da alohida HTML elementi emas. Ular dekoratsiya, badge, separator va icon kabi vazifalar uchun mos.

### `::first-letter`

```css
.article p:first-of-type::first-letter {
  float: left;
  margin-right: 8px;
  color: #2563eb;
  font-size: 52px;
  font-weight: 800;
  line-height: 0.85;
}
```

### `::first-line`

```css
.intro::first-line {
  font-weight: 700;
  color: #1e3a8a;
}
```

### `::selection`

Foydalanuvchi matnni belgilaganda rangni o‘zgartirish mumkin.

```css
::selection {
  background: #bfdbfe;
  color: #1e3a8a;
}
```

---

## 9. Pseudo-class va pseudo-element farqi

| Turi | Yozilishi | Vazifasi |
|---|---|---|
| Pseudo-class | `:hover` | Element holatini tanlaydi |
| Pseudo-class | `:nth-child(2)` | Element joylashuvini tanlaydi |
| Pseudo-element | `::before` | Virtual qism yaratadi |
| Pseudo-element | `::first-letter` | Elementning birinchi harfini tanlaydi |

Misol:

```css
/* Holat: tugma ustiga kelish */
.button:hover {
  background: #1d4ed8;
}

/* Virtual dekorativ chiziq */
.button::after {
  content: "";
  display: block;
  height: 2px;
  background: #22d3ee;
}
```

---

## 10. Specificity — qaysi qoida yutadi?

Bir elementga bir nechta qoida mos kelganda specificity, ya’ni selector aniqligi ishlaydi.

```html
<p id="main-text" class="important-text">Academy</p>
```

```css
p {
  color: green;
}

.important-text {
  color: blue;
}

#main-text {
  color: red;
}
```

Natija qizil bo‘ladi, chunki ID selector class va tag selectoridan ustun.

Umumiy tartib:

1. universal selector va inheritance;
2. tag selector;
3. class, attribute va pseudo-class;
4. ID selector;
5. inline style;
6. `!important`.

`!important`ni odatiy yechim sifatida ishlatmang. Avval selectorni to‘g‘ri va aniq yozing.

### Natija

<div style="margin:16px 0;padding:16px;border-left:4px solid #ef4444;border-radius:8px;background:#fee2e2;color:#991b1b;font-weight:700">ID selector eng yuqori specificity sababli bu rangni yutadi.</div>

---

## 11. Amaliy loyiha: interactive course navigation

### HTML

```html
<nav class="course-nav" aria-label="Kurs darslari">
  <a class="course-nav__item course-nav__item--active" href="#lesson-1">
    <span class="course-nav__number">1</span>
    <span>CSS ga kirish</span>
  </a>
  <a class="course-nav__item" href="#lesson-2">
    <span class="course-nav__number">2</span>
    <span>Ranglar va gradientlar</span>
  </a>
  <a class="course-nav__item" href="#lesson-3">
    <span class="course-nav__number">3</span>
    <span>Shriftlar</span>
  </a>
</nav>
```

### CSS

```css
.course-nav {
  width: min(100%, 420px);
  margin: 20px 0;
  padding: 8px;
  border: 1px solid #dbeafe;
  border-radius: 16px;
  background: #ffffff;
}

.course-nav__item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 14px;
  border-radius: 10px;
  color: #475569;
  text-decoration: none;
  transition: color 180ms ease, background-color 180ms ease;
}

.course-nav__item:hover {
  background: #eff6ff;
  color: #1d4ed8;
}

.course-nav__item:focus-visible {
  outline: 3px solid #22d3ee;
  outline-offset: 2px;
}

.course-nav__item--active {
  background: #2563eb;
  color: #ffffff;
  font-weight: 700;
}

.course-nav__number {
  display: grid;
  width: 28px;
  height: 28px;
  place-items: center;
  flex-shrink: 0;
  border-radius: 50%;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 13px;
  font-weight: 800;
}

.course-nav__item--active .course-nav__number {
  background: #ffffff;
}

.course-nav__item--active::after {
  position: absolute;
  right: 14px;
  content: "✓";
  color: #bfdbfe;
}
```

### Natija

<nav style="width:min(100%,420px);margin:20px 0;padding:8px;border:1px solid #dbeafe;border-radius:16px;background:white">
  <a href="#lesson-1" style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:10px;background:#2563eb;color:white;text-decoration:none;font-weight:700"><span style="display:grid;width:28px;height:28px;place-items:center;border-radius:50%;background:white;color:#1d4ed8;font-size:13px;font-weight:800">1</span><span>CSS ga kirish</span><span style="margin-left:auto;color:#bfdbfe">✓</span></a>
  <a href="#lesson-2" style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:10px;color:#475569;text-decoration:none"><span style="display:grid;width:28px;height:28px;place-items:center;border-radius:50%;background:#dbeafe;color:#1d4ed8;font-size:13px;font-weight:800">2</span><span>Ranglar va gradientlar</span></a>
  <a href="#lesson-3" style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:10px;color:#475569;text-decoration:none"><span style="display:grid;width:28px;height:28px;place-items:center;border-radius:50%;background:#dbeafe;color:#1d4ed8;font-size:13px;font-weight:800">3</span><span>Shriftlar</span></a>
</nav>

---

## 12. Ko‘p uchraydigan xatolar

### Class oldidan nuqta yozmaslik

```css
/* To‘g‘ri */
.card {
  padding: 20px;
}

/* Noto‘g‘ri: bu card tegini qidiradi */
card {
  padding: 20px;
}
```

### `:hover`ni noto‘g‘ri joyga yozish

```css
/* To‘g‘ri */
.button:hover {
  background: #1d4ed8;
}
```

### Pseudo-elementga `content` bermaslik

`::before` va `::after` `content` bo‘lmasa ko‘rinmaydi.

```css
.title::before {
  content: "";
}
```

### `!important` bilan muammoni yashirish

Avval selectorlar specificity’sini tekshiring. `!important` keyinchalik override qilishni qiyinlashtiradi.

### Link va button focus holatini olib tashlash

Klaviatura foydalanuvchilari uchun focus indicator saqlanib qolishi kerak.

---

## 13. Mustahkamlash topshiriqlari

### Topshiriq 1: Button states

Bitta button yarating va unga oddiy, hover, active, focus-visible va disabled holatlarini bering.

### Topshiriq 2: Kurslar ro‘yxati

`nth-child(even)` bilan juft cardlarga boshqa fon, `first-child` bilan birinchi cardga maxsus border bering.

### Topshiriq 3: Attribute form

Email, password va submit inputlardan iborat forma yarating. Har birini `[type]` selector yordamida alohida bezang.

### Topshiriq 4: Pseudo-element badge

Kurs cardining yuqori o‘ng burchagiga `::after` yordamida “Yangi” badge qo‘shing.

### Topshiriq 5: Navigation

3 ta dars havolasidan iborat navigation yarating. Faol darsga class, qolganlariga hover va focus holatlarini yozing.

---

## 14. Uyga vazifa: interactive course card

Kurs card yarating. Unda:

- kurs rasmi yoki SVG ikonka;
- kurs nomi va darajasi;
- “Boshlash” tugmasi;
- hover paytida border, rang va shadow o‘zgarishi;
- `::before` yoki `::after` orqali dekorativ belgi;
- `:focus-visible` holati;
- `nth-child` yordamida cardlar orasida rang farqi;
- mobile ekranda ham to‘g‘ri ko‘rinish

bo‘lsin.

Koddan keyin natijani brauzerda tekshiring va har bir selector qaysi elementga ta’sir qilayotganini yozib chiqing.

---

## Dars xulosasi

Bugun selectorlar yordamida kerakli elementni aniq tanlashni, descendant, child, sibling va attribute selectorlardan foydalanishni o‘rgandik. `:hover`, `:focus-visible`, `:active`, `:checked` va `:nth-child` orqali interaktiv holatlar yaratdik. `::before` va `::after` bilan HTML’ni ko‘paytirmasdan dekorativ elementlar qo‘shdik. Yakunda kurs navigation’ini amaliy tarzda yaratdik.

Keyingi darsda `display`, block, inline, inline-block va elementlarning sahifadagi joylashuvini o‘rganamiz.
