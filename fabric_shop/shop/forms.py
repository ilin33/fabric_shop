from django import forms
from .models import Product, ProductComment


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        has_variants = False
        has_color_variants = False
        has_size_variants = False

        # Якщо ми редагуємо існуючий об'єкт
        if self.instance and self.instance.pk:
            has_variants = self.instance.has_variants
            has_color_variants = self.instance.has_color_variants
            has_size_variants = self.instance.has_size_variants

        # Якщо створення нового — пробуємо дістати з POST
        if 'has_variants' in self.data:
            has_variants = self.data.get('has_variants') in ['true', 'True', '1', 'on']

        # Якщо є варіанти, але не має кольору чи розміру — ставимо required = False для відповідних полів
        # І навпаки — якщо є варіанти кольору/розміру, то required = True для них
        if has_variants:
            self.fields['color'].required = has_color_variants
            self.fields['size'].required = has_size_variants
            self.fields['price'].required = True
            self.fields['quantity'].required = True
        else:
            # Якщо варіантів немає — всі ці поля не обов’язкові
            for field in ['color', 'size', 'price', 'quantity']:
                self.fields[field].required = False

    class Media:
        js = ('admin/js/product_admin.js',)


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ваш коментар...'}),
        }