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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class ProductView(View):
    def get(self, request ,slug):
        selected_product = get_object_or_404(Product, slug=slug)
        context = {
            "product": selected_product
        }
        return render(request , "store/product_detail.html",context)
    def post(self,request , slug):
        pass

class CategoryView(ListView):
    template_name= "store/store.html"
    model = Product
    context_object_name = "products"
    def get_queryset(self):
        base_query = super().get_queryset()
        slug = self.kwargs["slug"]
        return base_query.filter(category__slug=slug)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]
        context["category_name"] = Category.objects.get(slug=slug)
        return context
    
    