from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShippingAddressForm
from .models import ShippingAddress
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def success(request):
    return render(request , "payment/payment-success.html")

def failed(request):
    return render(request , "payment/payment-failed.html")

def checkout(request):
    return render(request , "payment/checkout.html")

class CheckoutView(LoginRequiredMixin,View):
    login_url = "account-app:user-login"
    def get_shipping(self, user):
        try: 
            shipping = ShippingAddress.objects.get(user = user)
        
        except ShippingAddress.DoesNotExist:
            shipping = None
        return shipping
    def get(self , request):
        shipping = self.get_shipping(request.user)
        form = ShippingAddressForm(instance=shipping)
        return render(request, "payment/checkout.html" , {"form" : form})

    def post(self , request):
        shipping = self.get_shipping(request.user)
        form = ShippingAddressForm(request.POST,instance=shipping)
        if form.is_valid():
            wait = form.save(commit= False)

            wait.user = request.user
            wait.save()
            return redirect()
        return render(request , "payment/checkout.html")