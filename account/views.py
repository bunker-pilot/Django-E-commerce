from django.shortcuts import render, get_object_or_404
from .forms import CreateUserForm
from django.views import View 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request , "account/registeration/register.html" , {"form":form})
        
    def post(self,reuqest):
        form = CreateUserForm(reuqest.POST)
        if form.is_valid():
            form.save()
        return render(request , "account/registeration/register.html" , {"form":form})

