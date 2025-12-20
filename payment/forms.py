from django import forms
from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress

        exclude = ["user"]
        labels = {
            "full_name" : "Full name*",
            "email" : "Email*",
            "address1":"Address1 *",
            "city": "City*",
            "zip_code":"Zip code*"
        }