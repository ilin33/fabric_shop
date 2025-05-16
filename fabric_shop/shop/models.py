from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='slider_images/')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title or f"Slide {self.pk}"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис категорії")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Картинка категорії")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL (slug)")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE, verbose_name="Категорія")
    name = models.CharField(max_length=100, verbose_name="Назва підкатегорії")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL (slug)")
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True, verbose_name="Картинка підкатегорії")

    class Meta:
        verbose_name = "Підкатегорія"
        verbose_name_plural = "Підкатегорії"

    def __str__(self):
        return f"{self.category.name} — {self.name}"


class Product(models.Model):
    UNITS = [
        ('cm', 'См'),
        ('m', 'М'),
        ('mm', 'Мм'),
        ('kg', 'Кг'),
        ('g', 'Г'),
        ('pcs', 'Шт')
    ]

    subcategory = models.ForeignKey(Subcategory, related_name="products", on_delete=models.CASCADE,
                                    verbose_name="Підкатегорія")
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    description = models.TextField(blank=True, verbose_name="Опис")
    has_variants = models.BooleanField(default=False, verbose_name="Має варіанти")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна", null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Картинка")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL (slug)")
    color = models.CharField(max_length=50, blank=True, verbose_name="Колір")
    size = models.CharField(max_length=50, blank=True, verbose_name="Розмір")
    quantity = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Кількість на складі")
    unit_of_measurement = models.ForeignKey('UnitOfMeasurement', on_delete=models.SET_NULL, null=True, blank=True,
                                            verbose_name="Одиниця вимірювання")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

    def clean(self):
        if self.has_variants:
            errors = {}
            if self.price:
                errors['price'] = 'Не потрібно вказувати ціну, якщо є варіанти.'
            if self.quantity:
                errors['quantity'] = 'Не потрібно вказувати кількість, якщо є варіанти.'
            if self.color:
                errors['color'] = 'Не потрібно вказувати колір, якщо є варіанти.'
            if self.size:
                errors['size'] = 'Не потрібно вказувати розмір, якщо є варіанти.'
            if errors:
                raise ValidationError(errors)

    @property
    def has_color_variants(self):
        return self.variants.filter(color__gt='').exists()

    @property
    def has_size_variants(self):
        return self.variants.filter(size__gt='').exists()



class ProductVariant(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=50, verbose_name="Колір", blank=True)
    size = models.CharField(max_length=50, verbose_name="Розмір", blank=True)
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість на складі")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна", null=True, blank=True)
    image = models.ImageField(upload_to='product_variants/', blank=True, null=True, verbose_name="Картинка")

    class Meta:
        verbose_name = "Варіант товару"
        verbose_name_plural = "Варіанти товарів"
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.color or 'Без кольору'}, {self.size or 'Без розміру'}"

    @property
    def unit_of_measurement(self):
        return self.product.unit_of_measurement




class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва")
    abbreviation = models.CharField(max_length=10, verbose_name="Скорочення", unique=True)

    def __str__(self):
        return self.abbreviation

    class Meta:
        verbose_name = "Одиниця вимірювання"
        verbose_name_plural = "Одиниці вимірювання"


class ProductComment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коментар до товару"
        verbose_name_plural = "Коментарі до товарів"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} — {self.product.name}"


