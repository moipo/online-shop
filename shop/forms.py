from .models import Product, Order
from django import forms
from django.contrib.auth import User


class UserForm(models.Model):
    class Meta:
        model = User
        fields = ["username", "password"]

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ["slug"]
