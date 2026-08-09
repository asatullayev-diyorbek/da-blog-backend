from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("quizzes", "0002_gamification"), ("courses", "0002_initial")]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="category",
            field=models.CharField(blank=True, max_length=100, verbose_name="Kategoriya"),
        ),
        migrations.AddField(
            model_name="quiz",
            name="course",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="quizzes", to="courses.course", verbose_name="Kurs"),
        ),
        migrations.AddField(
            model_name="quiz",
            name="topic",
            field=models.CharField(blank=True, max_length=150, verbose_name="Asosiy mavzu"),
        ),
        migrations.AddField(
            model_name="question",
            name="difficulty",
            field=models.CharField(choices=[("easy", "Oson"), ("medium", "O'rta"), ("hard", "Qiyin")], default="easy", max_length=20, verbose_name="Qiyinlik"),
        ),
        migrations.AddField(
            model_name="question",
            name="topic",
            field=models.CharField(blank=True, max_length=150, verbose_name="Mavzu"),
        ),
    ]
