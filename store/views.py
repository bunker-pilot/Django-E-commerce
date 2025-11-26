from django.shortcuts import render , get_object_or_404
from django.urls import reverse_lazy
from .models import Category, Product
from django.views.generic import ListView
from django.views import View
# Create your views here.

def categories(request):
    all_categories = Category.objects.all()

    return {"all_categories": all_categories}

class HomeView(ListView):
    template_name = "store/store.html"
    model = Product
    context_object_name = "products"
    ordering = ["-modified_at"]

class ProductView(View):
    def get(self, request ,slug):
        selected_product = get_object_or_404(Product, slug=slug)
        context = {
            "product": selected_product
        }
        return render(request , "store/product_detail.html",context)
    def post(self,request , slug):
        pass

