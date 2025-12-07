from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name ="account-app"
urlpatterns = [
    path("register/" ,views.RegisterView.as_view(),  name = "register"),
    #Email verification logic
    path("email-verification/<str:uidb64>/<str:token>/",views.EmailVerificationView.as_view() , name ="email-verification"),
    path("email-verification-sent/" ,views.email_sent , name = "email-verification-sent" ),
    path("email-verification-success/" ,views.success, name = "email-verification-success"),
    path("email-verification-failed/" ,views.fail, name="email-verification-fail"),
    # Log in/ Log out
    path("user-login/" , views.LoginView.as_view() , name = "user-login"),
    path("logout/" , views.logout , name = "user-logout"),
    # Dashboard
    path("user-dashboard/" ,views.DashBoardView.as_view(),  name = "dashboard"),
    # Dashboard /Profile Management
    path("profile-management" , views.ProfileManagementView.as_view() , name = "profile-management"),
    # Dashboard / Delete acc
    path("del-account" , views.delete_account , name = "delete-user"),
    #Password reset view
    path("reset-password/" , auth_views.PasswordResetView.as_view(template_name = "account/password/password-reset.html") , name = "reset_password"),
    
    path("reset-password-sent" , auth_views.PasswordResetDoneView.as_view(template_name= "account/password/password-reset-sent.html") , name = "password_reset_done"),
    path("reset/<uidb64>/<token>/" , auth_views.PasswordResetConfirmView.as_view(template_name = "account/password/password-reset-form.html") , name = "password_reset_confirm"),
    path("pass-reset-complete" , auth_views.PasswordResetCompleteView.as_view(template_name = "account/password/password-reset-complete.html") , name = "password_reset_complete")
]
