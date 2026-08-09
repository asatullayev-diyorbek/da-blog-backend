from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("users", "0002_telegram_auth")]

    operations = [
        migrations.CreateModel(
            name="TelegramAuthSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token", models.CharField(max_length=64, unique=True)),
                ("status", models.CharField(choices=[("pending", "Kutilmoqda"), ("confirmation", "Tasdiq kutilmoqda"), ("confirmed", "Tasdiqlangan"), ("rejected", "Rad etilgan")], default="pending", max_length=20)),
                ("chat_id", models.BigIntegerField(blank=True, db_index=True, null=True)),
                ("username", models.CharField(blank=True, max_length=150)),
                ("full_name", models.CharField(blank=True, max_length=255)),
                ("avatar_file_id", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
                ("confirmed_at", models.DateTimeField(blank=True, null=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="telegram_auth_sessions", to="users.user")),
            ],
            options={"ordering": ["-created_at"], "verbose_name": "Telegram auth sessiyasi", "verbose_name_plural": "Telegram auth sessiyalari"},
        ),
    ]
