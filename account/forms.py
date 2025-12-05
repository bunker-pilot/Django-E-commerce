from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

# Register form
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

# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class UpdateUserForm(forms.ModelForm):
    password = None
    class Meta:
        model = User
        fields = ["username"  , "email"]
        exclude = ["password1" , "password2"]
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email