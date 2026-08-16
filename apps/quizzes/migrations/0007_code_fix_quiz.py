from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("quizzes", "0006_pointtransaction_arena")]

    operations = [
        migrations.AddField(
            model_name="quiz", name="quiz_type",
            field=models.CharField(choices=[("choice", "Variantli test"), ("code_fix", "Koddagi xatoni tuzatish")], default="choice", max_length=20, verbose_name="Test turi"),
        ),
        migrations.AddField(model_name="question", name="code_answers", field=models.JSONField(blank=True, default=list, verbose_name="Kod blankalari javoblari")),
        migrations.AddField(model_name="question", name="code_template", field=models.TextField(blank=True, verbose_name="Kod shabloni")),
    ]
