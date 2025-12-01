from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
# Create your views here.

def cart_summary(request):
    return render(request , "cart/cart.html")

def cart_add(request):
    cart = Cart(request)
    if request.POST.get("action") == "POST" :
        product_id = int(request.POST.get("product_id"))
        product_quantity = int(request.POST.get("product_quantity"))
        selected_product = get_object_or_404(Product, pk=product_id)
        cart.add(product = selected_product, product_quantity=product_quantity)
        response = JsonResponse({"qty" : len(cart)})
        return response
def cart_update(request):
    cart = Cart(request)
    if request.POST.get("action")== "POST":
        product_id = int(request.POST.get("product_id"))
        product_quantity = 1
        selected_product = get_object_or_404(Product , pk=product_id)
        cart.add(product = selected_product, product_quantity=product_quantity)
        response = JsonResponse({"total_price":cart.total_price() , "qty":len(cart)})
    return response

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get("action") == "POST":
        product_id = int(request.POST.get("product_id"))
        cart.delete(product_id)
        response = JsonResponse({"qty":len(cart) , "total_price":cart.total_price()})
    return response