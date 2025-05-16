from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product_variant']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'display_city', 'paid', 'status', 'created', 'updated']
    list_editable = ['paid', 'status']  # додаємо поля сюди, щоб їх можна було редагувати у списку
    list_filter = ['paid', 'status', 'created', 'updated']
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created', 'updated']

    def display_city(self, obj):
        return obj.city or obj.nova_poshta_city or obj.ukrposhta_city or "—"
    display_city.short_description = "Місто"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_variant', 'price', 'quantity']
