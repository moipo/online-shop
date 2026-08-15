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


class CheckoutForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Ваше имя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Иван"}),
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        label="Телефон",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+7 900 000 00 00"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "example@email.com"}
        ),
    )
    consent = forms.BooleanField(
        required=True,
        label="Я даю согласие на обработку персональных данных",
        error_messages={
            "required": "Необходимо согласие на обработку персональных данных."
        },
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}),
    )
    pickup_lng = forms.CharField(required=True, widget=forms.HiddenInput())
    pickup_lat = forms.CharField(required=True, widget=forms.HiddenInput())
    pickup_name = forms.CharField(required=False, widget=forms.HiddenInput())
    pickup_phone = forms.CharField(required=False, widget=forms.HiddenInput())
