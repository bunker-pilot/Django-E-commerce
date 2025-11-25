from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.

def bitch(request):
    return render(request , "store/store.html" , {})