from django import forms
from .models import Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        has_variants = False

        # Якщо ми редагуємо існуючий об'єкт
        if self.instance and self.instance.pk:
            has_variants = self.instance.has_variants

        # Якщо створення нового — пробуємо дістати з POST
        if 'has_variants' in self.data:
            has_variants = self.data.get('has_variants') in ['true', 'True', '1', 'on']

        # Залежно від has_variants виставляємо required
        make_optional = ['color', 'size', 'price', 'quantity']
        for field in make_optional:
            self.fields[field].required = not has_variants

    class Media:
        js = ('admin/js/product_admin.js',)
