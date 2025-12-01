from django.urls import path
from . import views

app_name ="account-app"
urlpatterns = [
    path("register/" ,views.register,  name = "register")
]
