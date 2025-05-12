from decimal import Decimal
from shop.models import Product, ProductVariant
from django.contrib import messages

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, variant_id=None, override_quantity=False):
        product_id = str(product.id)
        key = f"{product_id}:{variant_id}" if variant_id else product_id

        # Отримуємо поточну кількість товару в кошику
        current_quantity = self.cart.get(key, {}).get('quantity', 0)
        total_quantity = current_quantity + quantity if not override_quantity else quantity

        # Якщо товар має варіанти
        if variant_id:
            variant = ProductVariant.objects.get(id=variant_id)

            # Перевіряємо залишки
            if variant.quantity < total_quantity:
                messages.error(self.request, f"Недостатньо товару на складі: {variant.quantity} одиниць доступно.")
                return

            if key not in self.cart:
                self.cart[key] = {'quantity': 0, 'price': str(variant.price), 'variant_id': variant_id}

            self.cart[key]['quantity'] = total_quantity if override_quantity else self.cart[key]['quantity'] + quantity

        else:
            # Перевіряємо залишки для звичайного товару
            if product.quantity < total_quantity:
                messages.error(self.request, f"Недостатньо товару на складі: {product.quantity} одиниць доступно.")
                return

            if key not in self.cart:
                self.cart[key] = {'quantity': 0, 'price': str(product.price), 'variant_id': None}

            self.cart[key]['quantity'] = total_quantity if override_quantity else self.cart[key]['quantity'] + quantity

        self.save()

    def remove(self, product_id, variant_id=None):
        key = f"{product_id}:{variant_id}" if variant_id else str(product_id)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __iter__(self):
        for key, item in self.cart.items():
            product_id, *variant = key.split(":")
            product = Product.objects.get(id=product_id)
            item['product'] = product

            # Додаємо variant лише якщо він реально існує
            if variant and item.get('variant_id'):
                try:
                    variant_obj = ProductVariant.objects.get(id=item['variant_id'])
                    item['variant'] = variant_obj
                    price = variant_obj.price
                except ProductVariant.DoesNotExist:
                    item['variant'] = None
                    price = product.price
            else:
                item['variant'] = None  # ← важливо!
                price = product.price

            item['price'] = price
            item['total_price'] = Decimal(price) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal('0')
        for item in self:
            total += item['total_price']
        return total
