from django.shortcuts import render, get_object_or_404
from .forms import CreateUserForm
from django.views import View 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
# Create your views here.

class RegisterView(CreateView):
    template_name= "account/register.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("store-app:store")
    #context_object_name= "form" // Automatically names it form  :)
"""
class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request , "account/register.html" , {"form":form})
        
    def post(self,reuqest):
        form = CreateUserForm(reuqest.POST)
        if form.is_valid():
            form.save()
        return render(request , "account/register.html" , {"form":form})
"""
