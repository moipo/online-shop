from .models import Product, Order
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ "first_name", "email", "password"]
        labels = {"first_name" : "Your name"}

        widgets= {
        'password' : forms.PasswordInput
        }

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ["slug"]
