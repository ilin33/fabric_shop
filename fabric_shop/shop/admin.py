from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SliderImage, Category, Subcategory,
    Product, ProductVariant, UnitOfMeasurement, ProductComment
)
from .forms import ProductAdminForm


class ImagePreviewMixin:
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Картинка"


@admin.register(SliderImage)
class SliderImageAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('title', 'image_preview')


@admin.register(Category)
class CategoryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'image_preview')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subcategory)
class SubcategoryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['name', 'category', 'image_preview']
    search_fields = ['name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['color', 'size', 'quantity', 'price', 'image' ]


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'subcategory', 'unit_of_measurement', 'image_preview', 'has_variants']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['subcategory']
    search_fields = ['name', 'description']

    # Показуємо інлайн для варіантів товарів, якщо has_variants = True
    def get_inline_instances(self, request, obj=None):
        if obj and obj.has_variants:  # Якщо продукт має варіанти
            return [ProductVariantInline(self.model, self.admin_site)]  # Додаємо інлайн для варіантів
        return []

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Викликає clean() перед збереженням
        super().save_model(request, obj, form, change)


@admin.register(ProductVariant)
class ProductVariantAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = [
        'product', 'color', 'size', 'quantity', 'price',
         'image_preview', 'get_unit_of_measurement'
    ]
    list_filter = ['product', 'color', 'size']
    search_fields = ['product__name', 'color', 'size']

    @admin.display(description="Одиниця вимірювання")
    def get_unit_of_measurement(self, obj):
        return obj.unit_of_measurement

@admin.register(UnitOfMeasurement)
class UnitOfMeasurementAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation']
    search_fields = ['name', 'abbreviation']

@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'product__name')
