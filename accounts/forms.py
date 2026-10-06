from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class BuyerRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'password1',
            'password2'
        ]


class SellerRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15)

    business_name = forms.CharField(
        max_length=150
    )

    business_description = forms.CharField(
        widget=forms.Textarea
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'password1',
            'password2'
        ]
