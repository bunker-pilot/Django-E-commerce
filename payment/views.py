from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.


def success(request):
    return render(request , "payment/payment-success.html")

def failed(request):
    return render(request , "payment/payment-failed.html")