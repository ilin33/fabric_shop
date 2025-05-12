from decimal import Decimal
from shop.models import Product, ProductVariant
from django.contrib import messages

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, request, product, quantity=1, variant_id=None, override_quantity=False):
        product_id = str(product.id)
        key = f"{product_id}:{variant_id}" if variant_id else product_id

        # Якщо товар має варіанти
        if variant_id:
            variant = ProductVariant.objects.get(id=variant_id)

            # Перевіряємо залишки
            if variant.quantity < quantity:
                messages.error(request, f"Недостатньо товару на складі: {variant.quantity} одиниць доступно.")
                return  # Ви можете замінити повідомлення на переадресацію або інше

            # Перевіряємо, скільки вже є в кошику
            current_quantity = self.cart.get(key, {}).get('quantity', 0)
            if current_quantity + quantity > variant.quantity:
                messages.error(request,
                               f"Не можна додати більше товару, ніж є на складі. Максимум {variant.quantity - current_quantity} одиниць доступно.")
                return

            # Якщо товару не вистачає, припиняємо додавання
            if key not in self.cart:
                self.cart[key] = {'quantity': 0, 'price': str(variant.price), 'variant_id': variant_id}

            if override_quantity:
                self.cart[key]['quantity'] = quantity
            else:
                self.cart[key]['quantity'] += quantity

        # Для товарів без варіантів
        else:
            # Перевіряємо залишки для звичайного товару
            if product.quantity < quantity:
                messages.error(request, f"Недостатньо товару на складі: {product.quantity} одиниць доступно.")
                return  # Ви можете замінити повідомлення на переадресацію або інше

            # Перевіряємо, скільки вже є в кошику
            current_quantity = self.cart.get(key, {}).get('quantity', 0)
            if current_quantity + quantity > product.quantity:
                messages.error(request,
                               f"Не можна додати більше товару, ніж є на складі. Максимум {product.quantity - current_quantity} одиниць доступно.")
                return

            if key not in self.cart:
                self.cart[key] = {'quantity': 0, 'price': str(product.price), 'variant_id': None}

            if override_quantity:
                self.cart[key]['quantity'] = quantity
            else:
                self.cart[key]['quantity'] += quantity

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

            if variant and item['variant_id']:
                variant_obj = ProductVariant.objects.get(id=item['variant_id'])
                item['variant'] = variant_obj
                price = variant_obj.price
            else:
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
