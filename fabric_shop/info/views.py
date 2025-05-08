from django.shortcuts import render, redirect
from .models import SiteInfo, Testimonial
from .forms import TestimonialForm

from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def about_view(request):
    # Отримуємо дані для сайту
    site_info = SiteInfo.objects.first()
    # Отримуємо всі відгуки, сортуємо за датою створення (за спаданням)
    testimonials = Testimonial.objects.all().order_by('-created_at')

    # Пагінація
    paginator = Paginator(testimonials, 5)  # 5 відгуків на сторінку
    page_number = request.GET.get('page')  # Отримуємо номер сторінки з параметрів URL
    try:
        page_obj = paginator.get_page(page_number)  # Отримуємо об'єкт сторінки
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)  # Якщо сторінка не ціле число, показуємо першу
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)  # Якщо сторінка порожня, показуємо останню

    # Якщо форма надіслана (метод POST)
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Створюємо форму з даними POST
            form = TestimonialForm(request.POST)
            if form.is_valid():
                # Зберігаємо новий відгук
                testimonial = form.save(commit=False)
                testimonial.user = request.user  # Прив'язуємо відгук до поточного користувача
                testimonial.save()
                # Перенаправляємо на сторінку "Про нас"
                return redirect('info:about')  # Перенаправлення на правильну сторінку
        else:
            # Якщо користувач не авторизований, перенаправляємо на сторінку входу
            return redirect('login')
    else:
        # Якщо форма не була надіслана, створюємо порожню форму
        form = TestimonialForm()

    # Повертаємо шаблон з даними для відображення
    return render(request, 'info/about.html', {
        'site_info': site_info,
        'page_obj': page_obj,  # Передаємо об'єкт сторінки в шаблон
        'form': form,
    })