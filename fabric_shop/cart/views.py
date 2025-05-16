from django.shortcuts import redirect, get_object_or_404, render
from shop.models import Product, ProductVariant
from .cart import Cart
from django.http import JsonResponse
from django.contrib import messages


def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart = Cart(request)

    quantity = int(request.POST.get('quantity', 1))

    if product.has_variants:
        color = request.POST.get('color', '').strip()
        size = request.POST.get('size', '').strip()

        # Динамічно будуємо фільтр
        filter_kwargs = {'product': product}
        if color:
            filter_kwargs['color'] = color
        if size:
            filter_kwargs['size'] = size

        try:
            variant = ProductVariant.objects.get(**filter_kwargs)
        except ProductVariant.DoesNotExist:
            messages.error(request, "Вибраної комбінації немає.")
            return redirect('shop:product_detail', slug=product_slug)

        if variant.quantity < quantity:
            messages.error(request, f"Недостатньо товару на складі: {variant.quantity} одиниць доступно.")
            return redirect('shop:product_detail', slug=product_slug)

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