from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Category
# Create your views here.

def categories(request):
    all_categories = Category.objects.all()

    return {"all_categories": all_categories}

def bitch(request):
    return render(request , "store/store.html" , {})

