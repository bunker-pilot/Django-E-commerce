from django.urls import path
from . import views

urlpatterns = [
    path("customer-details/", views.CustomerInfo.as_view() , name = "payment_customer_details"),
    path("checkout/", views.CheckoutView.as_view() , name ="payment_checkout"),
    path("stripe/webhook/" , views.stripe_webhook, name="stripe-webhook"),
    path("success/" , views.success , name= "payment_success"),
    path("failed/" , views.failed , name = "payment_failed")
      
]
