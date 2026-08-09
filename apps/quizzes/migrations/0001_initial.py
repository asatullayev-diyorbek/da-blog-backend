from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("courses", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Sarlavha")),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
                ("description", models.TextField(blank=True, verbose_name="Tavsif")),
                ("time_limit", models.PositiveIntegerField(default=0, verbose_name="Vaqt limiti (soniya)")),
                ("pass_score", models.PositiveSmallIntegerField(default=60, verbose_name="O'tish foizi")),
                ("randomize_questions", models.BooleanField(default=False, verbose_name="Savollarni aralashtirish")),
                ("published", models.BooleanField(default=True, verbose_name="Faol")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("lesson", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="quizzes", to="courses.lesson", verbose_name="Dars")),
            ],
            options={"ordering": ["-created_at"], "verbose_name": "Test", "verbose_name_plural": "Testlar"},
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(verbose_name="Savol")),
                ("explanation", models.TextField(blank=True, verbose_name="Izoh")),
                ("order", models.PositiveSmallIntegerField(default=1, verbose_name="Tartib")),
                ("quiz", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="questions", to="quizzes.quiz")),
            ],
            options={"ordering": ["order", "id"], "verbose_name": "Savol", "verbose_name_plural": "Savollar"},
        ),
        migrations.CreateModel(
            name="AnswerOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=1000, verbose_name="Variant")),
                ("is_correct", models.BooleanField(default=False, verbose_name="To'g'ri javob")),
                ("order", models.PositiveSmallIntegerField(default=1, verbose_name="Tartib")),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="quizzes.question")),
            ],
            options={"ordering": ["order", "id"], "verbose_name": "Javob varianti", "verbose_name_plural": "Javob variantlari"},
        ),
        migrations.CreateModel(
            name="QuizAttempt",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("guest_id", models.CharField(blank=True, db_index=True, max_length=128)),
                ("answers", models.JSONField(blank=True, default=dict)),
                ("score", models.PositiveSmallIntegerField(default=0)),
                ("correct_answers", models.PositiveSmallIntegerField(default=0)),
                ("total_questions", models.PositiveSmallIntegerField(default=0)),
                ("passed", models.BooleanField(default=False)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("quiz", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attempts", to="quizzes.quiz")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="quiz_attempts", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-started_at"], "verbose_name": "Test urinishi", "verbose_name_plural": "Test urinishlari"},
        ),
    ]
