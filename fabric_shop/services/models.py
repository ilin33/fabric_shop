from django.db import models

class Service(models.Model):
    name = models.CharField("Назва послуги", max_length=200)
    image = models.ImageField("Фото", upload_to="services/")
    description = models.TextField("Опис")
    price = models.DecimalField("Ціна", max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"

    def __str__(self):
        return self.name
