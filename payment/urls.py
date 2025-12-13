from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view() , name = "payment_checkout"),
    path("success/" , views.success , name= "payment_success"),
    path("failed/" , views.failed , name = "payment_failed")
    
]
