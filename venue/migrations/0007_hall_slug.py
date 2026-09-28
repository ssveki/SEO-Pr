from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("venue", "0006_hall_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="hall",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Заполнится автоматически из названия. Можно переопределить.",
                max_length=120,
                null=True,
                unique=True,
                verbose_name="URL",
            ),
        ),
    ]