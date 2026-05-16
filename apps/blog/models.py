from django.db import models
from django.utils.text import slugify
from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    short_description = models.TextField(verbose_name="Qisqa tavsif")
    content = models.TextField(verbose_name="Kontent (Markdown)")
    cover = models.ImageField(upload_to="posts/covers/", verbose_name="Muqova")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Kategoriya",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="Teglar")
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Muallif",
    )
    published = models.BooleanField(default=False, verbose_name="Nashr qilingan")
    featured = models.BooleanField(default=False, verbose_name="Tanlangan")
    views = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar")
    read_time = models.PositiveSmallIntegerField(default=5, verbose_name="O'qish vaqti (daqiqa)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(blank=True, verbose_name="Email")
    content = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True, verbose_name="Tasdiqlangan")

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.post.title[:40]}"
