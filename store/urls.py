from django.urls import path
from . import views


app_name = "store-app"
urlpatterns = [
    path("" , views.HomeView.as_view(), name ="store"),
    path("product/<slug:slug>/" , views.ProductView.as_view() , name="product_detail"),
    path("search/<slug:slug>/" , views.CategoryView.as_view() , name = "category_search")
]
