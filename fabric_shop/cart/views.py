from django.shortcuts import redirect, get_object_or_404, render
from shop.models import Product, ProductVariant
from .cart import Cart
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlencode


def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))

    # Параметри для повернення назад у разі помилки
    redirect_params = {}

    if product.has_variants:
        color = request.POST.get('color', '').strip()
        size = request.POST.get('size', '').strip()

        if product.has_color_variants and not color:
            messages.error(request, "Будь ласка, виберіть колір.")
            redirect_params['color'] = ''
        else:
            redirect_params['color'] = color

        if product.has_size_variants and not size:
            messages.error(request, "Будь ласка, виберіть розмір.")
            redirect_params['size'] = ''
        else:
            redirect_params['size'] = size

        # Якщо відсутній обов'язковий параметр — повертаємо користувача назад
        if (product.has_color_variants and not color) or (product.has_size_variants and not size):
            url = reverse('shop:product_detail', kwargs={'slug': product_slug})
            return redirect(f'{url}?{urlencode(redirect_params)}')

        # Спробуємо знайти варіант
        try:
            variant = ProductVariant.objects.get(product=product, color=color, size=size)
        except ProductVariant.DoesNotExist:
            messages.error(request, "Такої комбінації кольору та розміру немає.")
            url = reverse('shop:product_detail', kwargs={'slug': product_slug})
            return redirect(f'{url}?{urlencode(redirect_params)}')

        if variant.quantity < quantity:
            messages.error(request, f"Недостатньо товару на складі: {variant.quantity} одиниць доступно.")
            url = reverse('shop:product_detail', kwargs={'slug': product_slug})
            return redirect(f'{url}?{urlencode(redirect_params)}')

        cart.add(product=product, variant_id=variant.id, quantity=quantity)

    else:
        if product.quantity < quantity:
            messages.error(request, f"Недостатньо товару на складі: {product.quantity} одиниць доступно.")
            return redirect('shop:product_detail', slug=product_slug)

        cart.add(product=product, quantity=quantity)

    messages.success(request, 'Товар успішно додано до кошика!')
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {
        'cart': cart
    })

def remove_from_cart(request, product_id, variant_id=None):
    cart = Cart(request)

    if variant_id:
        # Якщо вказано variant_id — видаляємо конкретний варіант
        variant = get_object_or_404(ProductVariant, id=variant_id, product_id=product_id)
        cart.remove(product_id=product_id, variant_id=variant_id)
    else:
        # Якщо variant_id не передано — видаляємо сам продукт (без варіантів)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product_id=product_id)

    return redirect('cart:cart_detail')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

def update_cart(request, product_id, variant_id=None):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))  # Витягуємо нову кількість

    # Оновлюємо товар у кошику
    cart.add(product=Product.objects.get(id=product_id), variant_id=variant_id, quantity=quantity, override_quantity=True)

    # Повертаємо нові дані для оновлення
    total_price = cart.get_total_price()
    item_total_price = next(item['total_price'] for item in cart if item['product'].id == product_id and (item['variant'].id if variant_id else None) == variant_id)

    return JsonResponse({
        'total_price': item_total_price,
        'total_price_all': total_price
    })