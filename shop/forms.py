from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows":3}))