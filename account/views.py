from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from .forms import CreateUserForm
from django.views import View 
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes , force_str
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.urls import reverse_lazy
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
            # email verification setup
            current = get_current_site(request)
            subject = "Email verification"
            message = render_to_string("account/registeration/email_verification.html" , {
                "user" : user,
                "domain": current.domain,
                "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                "token":account_activation_token.make_token(user),

            })

            user.email_user(message= message , subject=subject)

            return redirect("account-app:email-verification-sent")
        return render(request , "account/registeration/register.html" , {"form":form})

class EmailVerificationView(View):
    def get(self,request , uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            
            return redirect("account-app:email-verification-success")
        else:
            return redirect("account-app:email-verification-fail")

    def post(self, uibd64,token):
        pass 

def email_sent(request):
    return render(request,"account/registeration/email-verification-sent.html")
def success(request):
    return render(request,"account/registeration/email-verification-success.html")

def fail(request):
    return render(request,"account/registeration/email-verification-fail.html")