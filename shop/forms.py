from .models import Product, Order, ShippingAddress
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
        first_name = {
        "required" : True
        }


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ["slug"]

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['country', 'city', 'address', 'zip_code']
        labels = {"zip_code" : "zip code"}

        widgets = {
        'country' :  forms.TextInput(attrs = {'class' : 'form-control'} ),
        'city' :  forms.TextInput(attrs = {'class' : 'form-control'} ),
        'address' :  forms.TextInput(attrs = {'class' : 'form-control'} ),
        'zip_code' :  forms.TextInput(attrs = {'class' : 'form-control'} ),
        }
