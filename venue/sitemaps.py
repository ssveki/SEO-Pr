from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Hall, Poster


class StaticViewSitemap(Sitemap):
    """Статические страницы сайта (без /home/ и /booking/)."""
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        # name из venue/urls.py — те, что должны быть в индексе
        return [
            "venue:home",
            "venue:hall_list",
            "venue:poster_list",
            "venue:menu",
            "venue:events",
            "venue:gallery",
            "venue:contacts",
        ]

    def location(self, item):
        return reverse(item)


class HallSitemap(Sitemap):
    """Активные залы."""
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Hall.objects.filter(is_active=True)

    def lastmod(self, obj):
        # появится после ⭐-части (поле updated_at)
        return getattr(obj, "updated_at", None)

    def location(self, obj):
        # пока залы по pk. В Блоке 6 заменим на slug.
        return reverse("venue:hall_detail", kwargs={"pk": obj.pk})


class PosterSitemap(Sitemap):
    """Опубликованные события афиши."""
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Poster.objects.filter(is_published=True)

    def location(self, obj):
        # пока события по pk. В Блоке 6 заменим на slug.
        return reverse("venue:poster_detail", kwargs={"pk": obj.pk})