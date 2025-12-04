from django.urls import path
from . import views

app_name ="account-app"
urlpatterns = [
    path("register/" ,views.RegisterView.as_view(),  name = "register"),
    path("email-verification/<str:uidb64>/<str:token>/",views.EmailVerificationView.as_view() , name ="email-verification"),
    path("email-verification-sent/" ,views.email_sent , name = "email-verification-sent" ),
    path("email-verification-success/" ,views.success, name = "email-verification-success"),
    path("email-verification-failed/" ,views.fail, name="email-verification-fail"),
    path("user-login/" , views.LoginView.as_view() , name = "user-login")
]
