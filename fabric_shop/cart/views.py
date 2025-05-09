from django.shortcuts import redirect, get_object_or_404, render
from shop.models import Product, ProductVariant
from .cart import Cart
from django.http import JsonResponse


def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart = Cart(request)

    variant_id = request.POST.get('variant_id')  # або обробка через color/size
    color = request.POST.get('color')
    size = request.POST.get('size')

    # Ось тут витягуємо кількість з POST-запиту, або ставимо 1 за замовчуванням
    quantity = int(request.POST.get('quantity', 1))

    variant = None
    if product.has_variants and (color or size):
        variant = get_object_or_404(ProductVariant, product=product, color=color or '', size=size or '')
        # Додаємо товар з варіантом і кількістю
        cart.add(product=product, variant_id=variant.id, quantity=quantity)
    else:
        # Додаємо товар без варіантів і кількістю
        cart.add(product=product, quantity=quantity)

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