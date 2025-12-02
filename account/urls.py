from django.urls import path
from . import views

app_name ="account-app"
urlpatterns = [
    path("register/" ,views.RegisterView.as_view(),  name = "register"),
]
