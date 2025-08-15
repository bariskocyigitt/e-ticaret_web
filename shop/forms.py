from django import forms
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
