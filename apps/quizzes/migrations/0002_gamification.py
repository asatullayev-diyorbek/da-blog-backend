from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("quizzes", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Badge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.SlugField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=255)),
                ("icon", models.CharField(default="🏅", max_length=20)),
            ],
            options={"verbose_name": "Badge", "verbose_name_plural": "Badge'lar"},
        ),
        migrations.CreateModel(
            name="UserGamification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("total_points", models.PositiveIntegerField(default=0)),
                ("level", models.PositiveIntegerField(default=1)),
                ("current_streak", models.PositiveIntegerField(default=0)),
                ("last_activity_date", models.DateField(blank=True, null=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="gamification", to="users.user")),
            ],
            options={"ordering": ["-total_points", "user__username"], "verbose_name": "Gamification profili", "verbose_name_plural": "Gamification profillari"},
        ),
        migrations.CreateModel(
            name="PointTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("points", models.PositiveIntegerField()),
                ("reason", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("attempt", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="point_transactions", to="quizzes.quizattempt")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="point_transactions", to="users.user")),
            ],
            options={"ordering": ["-created_at"], "verbose_name": "XP harakati", "verbose_name_plural": "XP harakatlari"},
        ),
        migrations.CreateModel(
            name="UserBadge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("earned_at", models.DateTimeField(auto_now_add=True)),
                ("badge", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="users", to="quizzes.badge")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="badges", to="users.user")),
            ],
            options={"ordering": ["-earned_at"]},
        ),
        migrations.AddConstraint(
            model_name="userbadge",
            constraint=models.UniqueConstraint(fields=("user", "badge"), name="unique_user_badge"),
        ),
    ]
