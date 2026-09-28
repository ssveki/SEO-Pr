from django.db import migrations

from venue.utils import make_slug


def fill_slugs(apps, schema_editor):
    Poster = apps.get_model("venue", "Poster")
    for poster in Poster.objects.all():
        if not poster.slug:
            base = make_slug(poster.title)
            slug = base
            n = 1
            while Poster.objects.filter(slug=slug).exclude(pk=poster.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            poster.slug = slug
            poster.save(update_fields=["slug"])


def clear_slugs(apps, schema_editor):
    Poster = apps.get_model("venue", "Poster")
    Poster.objects.update(slug=None)


class Migration(migrations.Migration):

    dependencies = [
        ("venue", "0011_poster_slug"),
    ]

    operations = [
        migrations.RunPython(fill_slugs, clear_slugs),
    ]