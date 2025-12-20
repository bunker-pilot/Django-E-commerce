from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem
from store.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
from django.conf import settings
# Create your views here.

stripe.api_key = settings.STRIPE_PRIVATE_KEY

def success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("store-app:store")

    try : 
        session = stripe.checkout.Session.retrieve(session_id)
        order = Order.object.get(pk = session.metadata.get("order_id"))
    except Exception:
        return redirect("store-app:store")

    if (order.status).casefold() !="paid":
        return render(request , "payment/payment-processing.html" , {"order":order})
    elif (order.status).casefold() == "failed":
        return render(request , "payment/payment-failed.html", {"order":order})
    cart = Cart(request)
    cart.clear()
    return render(request , "payment/payment-success.html", {"order":order})

def failed(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("store-app:store")
    try :
        sesssion = stripe.checkout.Session.retrieve(session_id)
        order = Order.objects.get(pk = sesssion.metadata.get("order_id"))
    except Exception:
        return redirect("store-app:store")
    
    if (order.status).casefold() == "paid":
        return render(request , "payment/payment-success.html", {"order":order})
    
    elif (order.status).casefold() == "pending":
        return render(request , "payment/payment_processing.html", {"order":order})
    
    return render(request , "payment/payment-failed.html", {"order":order})

class CustomerInfo(LoginRequiredMixin,View):
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
        return render(request, "payment/customer_info.html" , {"form" : form})

    def post(self , request):
        shipping = self.get_shipping(request.user)
        form = ShippingAddressForm(request.POST,instance=shipping)
        if not form.is_valid():
            return render(request , "payment/customer_info.html")
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
                shipping_address=str(shipment_info.address1 + "\n" + (shipment_info.address2 or "") +"\n"
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
            request.session["order_id"] = order.id
            reqeust.session.modified = True
              
        return redirect("payment_checkout")

    
class CheckoutView(LoginRequiredMixin,View):
    login_url = "account-app:user-login"
    def get(self ,request):
        return render(request , "payment/checkout.html")
    def post(self, request):
        order = Order.objects.get(user = request.user, pk = request.session.get("order_id"))
        amount = order.amount_paid * 100
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
                    mode="payment",
                    line_items=[{
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "Order",
                            },
                            "unit_amount": amount,
                        },
                        "quantity": 1,
                    }],
                metadata = {
                    "order_id" : order.id,
                    "user_id" : request.user.id
                },
                success_url=request.build_absolute_uri( reverse_lazy("payment_success")) + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url = request.build_absolute_uri(reverse_lazy("payment_fail"))
            )
        return redirect(session.url)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(
            payload = payload, sig_header=sig_header,secret=endpoint_secret
        )
    except ValueError:
        return HttpResponse(status = 400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status = 400)

    if event["type"] =="checkout.session.completed":
        session = event["data"]["object"]
        order_id = session["metadata"]["order_id"]
        order = Order.objects.get(id = order_id)
        order.status = "paid"
        order.save()
    elif event["type"] == "payment_intent.payment_failed":
        session = event["data"]["object"]
        order_id = session["metadata"]["order_id"]
        order = Order.objects.get(id = order_id)
        order.status = "failed"
        order.save()

    return HttpResponse(status =200)



