from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.views import View 
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes , force_str
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.urls import reverse_lazy
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request , "account/registeration/register.html" , {"form":form})
        
    def post(self,request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active = False
            user.save()
            # email setup
            current = get_current_site(request)
            subject = "Jonkey:Verify your email"
            message = render_to_string("account/registeration/email_verification.html" , {
                "user" : user,
                "domain": current.domain,
                "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                "token":account_activation_token.make_token(user),

            })

            user.email_user(subject , message)

            return redirect("email-verification-sent")
        return render(request , "account/registeration/register.html" , {"form":form})

class EmailVerificationView(View):
    def get(self,request , uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        try:
            user = get_object_or_404(User , pk = uid)
        except User.DoesNotExist:
            user = None
        # success
        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("email-verification-success")
        #fail
        else:
            return redirect("email-verification-fail")

def email_sent(request):
    return render(request,"account/registeration/email-verification-sent.html")
def success(request):
    return render(request,"account/registeration/email-verification-success.html")

def fail(request):
    return render(request,"account/registeration/email-verification-failed.html")

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request , "account/login.html" , {"form":login_form})
    
    def post(self , request):
        login_form = LoginForm(request , data = request.POST )
        if login_form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(request , username = username , password =password)
            if user is not None:
                auth.login(request , user)
                return redirect("dashboard")
                
        return render(request , "account/login.html" , {"form":login_form})


def logout(request):
    auth.logout(request)
    return redirect("store-app:store")

class DashBoardView( LoginRequiredMixin , View):
    login_url = "account-app:user-login"
    def get(self, request):
        return render(request , "account/dashboard.html")

"""
Tutorial implementation
@login_required(login_url="account-app:user-login")
def DashBoard(request):
     return render(request , "account/dashboard.html")
"""

class ProfileManagementView(LoginRequiredMixin,View):
    login_url = "account-app:user-login"
    def get(self , request):
        form = UpdateUserForm(instance=request.user)
        return render(request , "account/profile_manage.html" ,{"form": form}) 
    
    def post(self, request):
        form = UpdateUserForm(request.POST, instance= request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        return render(request , "account/profile_manage.html" ,{"form": form}) 

@login_required(login_url="user-login")
def delete_account(request):
    user = User.objects.get(id = request.user.id)

    if request.method == "POST":
        user.delete()

        return redirect("store-app:store")
    return render(request , "account/delete_account.html")


