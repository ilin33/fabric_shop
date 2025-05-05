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
    variants = product.variants.all() if product.has_variants else []

    # Додаємо логіку перевірки, чи є хоч один варіант з color або size
    show_color = any(v.color for v in variants)
    show_size = any(v.size for v in variants)

    context = {
        'product': product,
        'variants': variants,
        'show_color': show_color,
        'show_size': show_size,
    }
    return render(request, 'shop/product_detail.html', context)

def add_to_cart(request, product_slug):
    # Логіка додавання товару в корзину
    product = get_object_or_404(Product, slug=product_slug)
    # Логіка для додавання товару до сесії або корзини користувача
    return redirect('shop:cart_detail')  # Перенаправлення до корзини або іншої сторінки