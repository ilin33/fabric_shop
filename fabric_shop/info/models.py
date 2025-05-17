from django.db import models
from django.contrib.auth.models import User

class SiteInfo(models.Model):
    about_text = models.TextField(verbose_name="Про нас")
    working_hours = models.CharField(max_length=255, verbose_name="Графік роботи")
    address = models.CharField(max_length=255, verbose_name="Адреса")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    image = models.ImageField(upload_to='site_images/', null=True, blank=True, verbose_name="Зображення")


    def __str__(self):
        return "Інформація про сайт"

    class Meta:
        verbose_name = "Інформація про сайт"
        verbose_name_plural = "Інформація про сайт"


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Відгук")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Відгук від {self.user.username}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField(verbose_name="Посилання")

    class Meta:
        verbose_name = "Соцмережа"
        verbose_name_plural = "Соцмережі"

    def __str__(self):
        return dict(self.PLATFORM_CHOICES).get(self.platform, self.platform)


class DeliveryAndPayment(models.Model):
    title = models.CharField("Заголовок сторінки", max_length=200, default="Доставка та оплата")
    content = models.TextField("Контент сторінки (HTML або текст)", help_text="Можна використовувати HTML")

    class Meta:
        verbose_name = "Сторінка доставки та оплати"
        verbose_name_plural = "Сторінка доставки та оплати"

    def __str__(self):
        return self.title
