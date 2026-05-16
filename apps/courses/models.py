from django.db import models
from django.utils.text import slugify
from apps.users.models import User
from apps.blog.models import Category


LEVEL_CHOICES = [
    ("Boshlang'ich", "Boshlang'ich"),
    ("O'rta", "O'rta"),
    ("Yuqori", "Yuqori"),
]

PRICE_CHOICES = [
    ("Bepul", "Bepul"),
    ("Pullik", "Pullik"),
]


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    short_description = models.TextField(verbose_name="Qisqa tavsif")
    cover = models.ImageField(upload_to="courses/covers/", verbose_name="Muqova")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
        verbose_name="Kategoriya",
    )
    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
        verbose_name="O'qituvchi",
    )
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Daraja")
    price = models.CharField(max_length=10, choices=PRICE_CHOICES, default="Bepul", verbose_name="Narx")
    duration = models.CharField(max_length=50, verbose_name="Davomiyligi")
    students = models.PositiveIntegerField(default=0, verbose_name="O'quvchilar soni")
    featured = models.BooleanField(default=False, verbose_name="Tanlangan")
    published = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def lessons_count(self):
        return self.lessons.count()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Kurs",
    )
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Tartib")
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(blank=True, max_length=255)
    duration = models.CharField(max_length=50, verbose_name="Davomiyligi")
    is_free = models.BooleanField(default=False, verbose_name="Bepul")
    video_id = models.CharField(max_length=50, blank=True, verbose_name="YouTube Video ID")
    content = models.TextField(blank=True, verbose_name="Kontent (Markdown)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ["course", "order"]
        unique_together = [["course", "slug"]]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} — {self.order}. {self.title}"
