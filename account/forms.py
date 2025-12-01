from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    email = forms.EmailField( required=True , max_length = 300)
    class Meta:
        model = User
        fields = ["username" , "email" , "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email
