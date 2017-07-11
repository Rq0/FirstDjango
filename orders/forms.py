from django import forms
from orders.models import ProductInBasket


class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)


class ProductInBasketForm(forms.ModelForm):

    class Meta:
        model = ProductInBasket
        fields = ("nmb", "session_key", "product")
        widgets = {
            "session_key": forms.HiddenInput(),
            "product": forms.HiddenInput()
        }
