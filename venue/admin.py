from django.contrib import admin

from .models import FAQ, BookingRequest, EventFormat, Hall, MenuPackage, Poster, Review


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = (
        "name", "line_number", "capacity_banquet", "area",
        "price_from", "order", "is_active",
    )
    list_editable = ("order", "is_active")
    fieldsets = (
        ("Основное", {
            "fields": ("name", "order", "is_active"),
        }),
        ("Описание", {
            "fields": ("short_description", "description", "features"),
        }),
        ("Параметры зала", {
            "fields": (
                "line_color", "line_number",
                "capacity_banquet", "capacity_buffet",
                "area", "price_from",
            ),
        }),
        ("Оформление", {
            "fields": ("image",),
        }),
        ("SEO (мета-теги)", {
            "fields": ("meta_title", "meta_description"),
            "description": (
                "Оставьте пустыми — title и description сгенерируются автоматически. "
                "Если заполните — будут использоваться ваши значения."
            ),
        }),
    )
    # ПОДСКАЗКА (Блок 6): когда добавите slug, раскомментируйте:
    # prepopulated_fields = {"slug": ("name",)}


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "date", "time", "schedule", "is_published")
    list_filter = ("is_published",)
    list_editable = ("is_published",)
    date_hierarchy = "date"


@admin.register(EventFormat)
class EventFormatAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)


@admin.register(MenuPackage)
class MenuPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price_per_person", "is_featured", "order")
    list_editable = ("is_featured", "order")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "event", "rating", "created_at", "is_published")
    list_filter = ("is_published", "rating")
    list_editable = ("is_published",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "date", "guests", "hall", "status", "created_at")
    list_filter = ("status", "hall", "date")
    list_editable = ("status",)
    search_fields = ("name", "phone", "comment")
    readonly_fields = ("created_at",)


admin.site.site_header = "Подземка — управление"
admin.site.site_title = "Подземка"
admin.site.index_title = "Контент сайта и заявки"