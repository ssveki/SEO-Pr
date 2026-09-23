def home(request):
    reviews = Review.objects.filter(is_published=True)
    context = {
        "halls": Hall.objects.filter(is_active=True),
        "formats": EventFormat.objects.all()[:6],
        "packages": MenuPackage.objects.filter(is_featured=True)[:3],
        "reviews": reviews[:6],
        "rating": reviews.aggregate(avg=Avg("rating"))["avg"],
        "reviews_count": reviews.count(),
        "faqs": FAQ.objects.all(),
        "posters": upcoming_posters()[:6],
        "form": BookingForm(),
        "meta_title": "Подземка — банкетный зал в Чите: лофт, андеграунд, мероприятия",
        "meta_description": (
            "Банкетный зал «Подземка» в Чите: лофт и андеграунд. Свадьбы, корпоративы, "
            "дни рождения, квизы. Узнайте свободные даты и забронируйте онлайн."
        ),
    }
    return render(request, "venue/home.html", context)


def hall_list(request):
    return render(request, "venue/hall_list.html", {
        "halls": Hall.objects.filter(is_active=True),
        "meta_title": "Залы для банкетов и мероприятий в Чите — Подземка",
        "meta_description": (
            "4 зала в стиле лофт и андеграунд: «Депо», «Тоннель», «Платформа», "
            "«Вестибюль». Фото, вместимость, цены. Забронируйте зал в «Подземке»."
        ),
    })


def hall_detail(request, pk):
    hall = get_object_or_404(Hall, pk=pk, is_active=True)
    others = Hall.objects.filter(is_active=True).exclude(pk=hall.pk)
    form = BookingForm(initial={"hall": hall})
    return render(request, "venue/hall_detail.html", {
        "hall": hall,
        "others": others,
        "form": form,
        "meta_title": getattr(hall, "get_meta_title", lambda: None)() or (
            f"{hall.name} — аренда зала в Чите | Подземка"
        ),
        "meta_description": getattr(hall, "get_meta_description", lambda: None)() or (
            f"{hall.short_description} Вместимость до {hall.capacity_banquet} гостей. "
            "Забронируйте в «Подземке»."
        ),
    })


def poster_list(request):
    return render(request, "venue/poster_list.html", {
        "posters": upcoming_posters(),
        "meta_title": "Афиша событий — квизы и вечеринки в Чите | Подземка",
        "meta_description": (
            "Квизы, вечеринки, концерты и зарядки в «Подземке». Смотрите расписание, "
            "покупайте билеты и приходите в наш лофт в Чите."
        ),
    })


def poster_detail(request, pk):
    poster = get_object_or_404(Poster, pk=pk, is_published=True)
    date_human = poster.date.strftime("%d.%m.%Y")
    return render(request, "venue/poster_detail.html", {
        "poster": poster,
        "is_past": not poster.schedule and poster.date < datetime.date.today(),
        "meta_title": f"{poster.title} — {date_human} | Афиша Подземки",
        "meta_description": (
            f"{poster.short_description} {date_human}, Чита. Билеты и бронь — на сайте «Подземки»."
        ),
    })


def menu(request):
    return render(request, "venue/menu.html", {
        "packages": MenuPackage.objects.all(),
        "meta_title": "Банкетное меню — сеты от 1900 ₽/гость | Подземка",
        "meta_description": (
            "Банкетные сеты «Подземки»: от классики до авторских форматов. "
            "Цены, состав, хиты. Подберём меню под ваш формат мероприятия."
        ),
    })


def events(request):
    return render(request, "venue/events.html", {
        "formats": EventFormat.objects.all(),
        "halls": Hall.objects.filter(is_active=True),
        "meta_title": "Форматы мероприятий — свадьбы, корпоративы | Подземка",
        "meta_description": (
            "Свадьбы, корпоративы, дни рождения и квизы в лофт-пространстве «Подземка» "
            "в Чите. Подберём зал и меню под ваш формат. Забронируйте дату."
        ),
    })


def gallery(request):
    photos = [
        {"src": "img/hall-depo.jpg", "caption": "Зал «Депо»"},
        {"src": "img/hall-tonnel.webp", "caption": "Зал «Тоннель»"},
        {"src": "img/hall-platforma.jpg", "caption": "Зал «Платформа»"},
        {"src": "img/hall-vestibul.jpg", "caption": "Бар «Вестибюль»"},
    ]
    return render(request, "venue/gallery.html", {
        "photos": photos,
        "meta_title": "Галерея — фото залов и мероприятий | Подземка Чита",
        "meta_description": (
            "Фотографии залов, банкетов, свадеб и вечеринок в «Подземке». "
            "Посмотрите, как выглядит ваше будущее мероприятие."
        ),
    })


def contacts(request):
    return render(request, "venue/contacts.html", {
        "meta_title": "Контакты — как добраться до «Подземки» в Чите",
        "meta_description": (
            "Адрес, телефон, часы работы и карта проезда до банкетного зала «Подземка» "
            "в Чите. Свяжитесь с нами удобным способом."
        ),
    })


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка принята! Перезвоним в течение 15 минут.")
            return redirect("venue:booking")
    else:
        form = BookingForm(initial={
            "hall": request.GET.get("hall"),
            "comment": request.GET.get("comment", ""),
            "guests": request.GET.get("guests"),
        })
    return render(request, "venue/booking.html", {
        "form": form,
        "meta_title": "Бронирование зала — оставить заявку | Подземка",
        "meta_description": (
            "Оставьте заявку на бронирование зала в «Подземке». Перезвоним в течение "
            "15 минут, подберём дату и формат."
        ),
    })