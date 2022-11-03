from .models import Product, Order
from django import forms


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ["slug"]
