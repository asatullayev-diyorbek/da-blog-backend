from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AddField(model_name="user", name="telegram_chat_id", field=models.BigIntegerField(blank=True, db_index=True, null=True, unique=True)),
        migrations.AddField(model_name="user", name="telegram_full_name", field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name="user", name="telegram_username", field=models.CharField(blank=True, max_length=150)),
        migrations.CreateModel(
            name="TelegramLoginCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=5, unique=True)),
                ("chat_id", models.BigIntegerField(db_index=True)),
                ("username", models.CharField(blank=True, max_length=150)),
                ("full_name", models.CharField(blank=True, max_length=255)),
                ("avatar_file_id", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
                ("used_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={"ordering": ["-created_at"], "verbose_name": "Telegram login kodi", "verbose_name_plural": "Telegram login kodlari"},
        ),
    ]
