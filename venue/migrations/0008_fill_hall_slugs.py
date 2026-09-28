from django.db import migrations

from venue.utils import make_slug


def fill_slugs(apps, schema_editor):
    Hall = apps.get_model("venue", "Hall")
    for hall in Hall.objects.all():
        if not hall.slug:
            base = make_slug(hall.name)
            slug = base
            n = 1
            while Hall.objects.filter(slug=slug).exclude(pk=hall.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            hall.slug = slug
            hall.save(update_fields=["slug"])


def clear_slugs(apps, schema_editor):
    Hall = apps.get_model("venue", "Hall")
    Hall.objects.update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ("venue", "0007_hall_slug"),
    ]

    operations = [
        migrations.RunPython(fill_slugs, clear_slugs),
    ]