from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# SEO-ЗАДАНИЕ (sitemap.xml) — Блок 4, подключим здесь же позже.

urlpatterns = [
    path("admin/", admin.site.urls),

    # robots.txt строго в корне, Content-Type: text/plain
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
        name="robots_txt",
    ),

    path("", include("venue.urls")),
]