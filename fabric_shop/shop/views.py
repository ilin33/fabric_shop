from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import SliderImage, Category

from django.conf import settings

def home(request):
    slides = SliderImage.objects.order_by('order')
    categories = Category.objects.all()
    context = {
        'slides': slides,
        'active_page': 'home',
        'categories': categories,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'shop/home.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.subcategories.all()
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'subcategories': subcategories
    })