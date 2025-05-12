from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email',
            'delivery_method', 'city', 'postal_code', 'address',
            'nova_poshta_city', 'nova_poshta_warehouse',
            'ukrposhta_city', 'ukrposhta_warehouse',
        ]
        widgets = {
            'delivery_method': forms.Select(attrs={'id': 'id_delivery_method'}),
        }
