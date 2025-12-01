from django.shortcuts import render, get_object_or_404
from .forms import CreateUserForm
from django.views import View
from django.urls import reverse_lazy
# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        
    def post(self,reuqest):
        form = CreateUserForm(reuqest.POST)
        if form.is_valid():
            form.save()
        return render(request , "account/register.html" , {"form":form})

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request , "account/register.html" , {"form":form})
