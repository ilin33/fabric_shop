from django.db import models
from django.conf import settings
from shop.models import ProductVariant

class Order(models.Model):
    DELIVERY_METHOD_CHOICES = [
        ('pickup', 'Самовивіз'),
        ('courier', 'Кур’єрська доставка'),
        ('nova_poshta', 'Нова Пошта'),
        ('ukrposhta', 'Укрпошта'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, default='pickup')

    # Кур'єрське або ручне введення адреси
    address = models.CharField(max_length=250, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    # Нова Пошта
    nova_poshta_city = models.CharField(max_length=100, blank=True)
    nova_poshta_warehouse = models.CharField(max_length=100, blank=True)

    # Укрпошта
    ukrposhta_city = models.CharField(max_length=100, blank=True)
    ukrposhta_warehouse = models.CharField(max_length=100, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product_variant}'

    def get_cost(self):
        return self.price * self.quantity
