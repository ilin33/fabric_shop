from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import SliderImage, Category, Subcategory, Product

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

def subcategory_detail(request, slug):
    subcategory = get_object_or_404(Subcategory, slug=slug)
    products = subcategory.products.all()
    return render(request, 'shop/subcategory_detail.html', {
        'subcategory': subcategory,
        'products': products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})