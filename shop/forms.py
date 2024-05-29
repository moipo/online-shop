from django import forms
from django.contrib.auth.models import User

from .models import Card, ShippingAddress


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=200,
        required=True,
        label="Your name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "email", "password"]
        labels = {"first_name": "Your name"}

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }
        fields_required = ["first_name", "email", "password"]


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["country", "city", "address", "zip_code"]
        labels = {"zip_code": "zip code"}

        widgets = {
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control"}),
        }


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["name_on_card", "number", "expiration_date", "cvv"]
        widgets = {
            "name_on_card": forms.TextInput(attrs={"class": "form-control"}),
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "expiration_date": forms.TextInput(attrs={"class": "form-control"}),
            "cvv": forms.TextInput(attrs={"class": "form-control"}),
        }
