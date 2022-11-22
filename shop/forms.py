from .models import Product, Order, ShippingAddress, Card
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ "first_name", "email", "password"]
        labels = {"first_name" : "Your name"}

        widgets= {
        'password' : forms.PasswordInput,
        'first_name' :  forms.TextInput(attrs = {'first_name' : 'form-control'} ),
        'email' :  forms.TextInput(attrs = {'email' : 'form-control'} ),
        'password' :  forms.TextInput(attrs = {'password' : 'form-control'} ),
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


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name_on_card', 'number', 'expiration_date', 'cvv']
        widgets = {
        'name_on_card' :  forms.TextInput(attrs = {'class' : 'form-control'} ),
        'number' :  forms.TextInput(attrs = {'class' : 'form-control'} ),
        'expiration_date' :  forms.TextInput(attrs = {'class' : 'form-control'} ),
        'cvv' :  forms.TextInput(attrs = {'class' : 'form-control'} ),
        }
