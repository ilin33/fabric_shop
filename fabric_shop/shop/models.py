from django.db import models


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