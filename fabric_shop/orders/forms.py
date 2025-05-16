from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name',  'phone_number', 'email',
            'delivery_method', 'city', 'postal_code', 'address',
            'nova_poshta_city', 'nova_poshta_warehouse',
            'ukrposhta_city', 'ukrposhta_warehouse',
        ]
        widgets = {
            'delivery_method': forms.Select(attrs={'id': 'id_delivery_method'}),
            'phone_number': forms.TextInput(attrs={'value': '+380'}),
        }
        labels = {
            'first_name': 'Ім’я',
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
            'phone_number': 'Номер телефону',
            'delivery_method': 'Спосіб доставки',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Зробити додаткові поля необов’язковими
        optional_fields = [
            'city', 'postal_code', 'address',
            'nova_poshta_city', 'nova_poshta_warehouse',
            'ukrposhta_city', 'ukrposhta_warehouse',
        ]
        for field in optional_fields:
            self.fields[field].required = False
