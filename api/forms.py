from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from api.models import SiteUser


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    date_of_birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = SiteUser
        fields = ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_picture')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())