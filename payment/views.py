from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem
from store.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from cart.cart import Cart
# Create your views here.


def success(request):
    if not request.session.get("order_submission"):
        return redirect("store-app:store")
    request.session.pop("order_submission" , None)
    cart = Cart(request)
    cart.clear()
    return render(request , "payment/payment-success.html")

def failed(request):
    return render(request , "payment/payment-failed.html")

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
        if request.session.get("order_submission"):
            return redirect("payment_success")
        shipping = self.get_shipping(request.user)
        form = ShippingAddressForm(request.POST,instance=shipping)
        if not form.is_valid():
            return render(request , "payment/checkout.html")
        cart = Cart(request)
        if len(cart) == 0:
            return redirect("store-app:store")
        with transaction.atomic():
            shipment_info = form.save(commit= False)
            shipment_info.user = request.user
            shipment_info.save()
            order =Order.objects.create(
                full_name= shipment_info.full_name,
                email = shipment_info.email,
                user = request.user,
                shipping_address=str(shipment_info.address1 + "\n" + shipment_info.address2 or "" +"\n"
                +shipment_info.city + "\n" + shipment_info.zip_code),
                amount_paid= cart.total_price()
            )
            
            for item in cart:
                order_item =OrderItem.objects.create(
                    order=order , product=item["product"],
                    product_name= item["product"].title ,quantity=item["qty"],
                    price=item["price"],
                    total_price= item["total_price"]
                )

        request.sesssion["order_submission"] =True        
        return redirect("payment_success")
