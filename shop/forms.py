from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Card, ShippingAddress


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Your name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    password = forms.CharField(
        max_length=128,
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if (
            User.objects.filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password, self.instance)
        return password

    class Meta:
        model = User
        fields = ["first_name", "email", "password"]
        labels = {"first_name": "Your name"}


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
