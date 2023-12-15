from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField, DateField, ImageField, CharField
from django.forms.widgets import PasswordInput, TextInput

from api.models import SiteUser


class SignupForm(UserCreationForm):
    """
    A form allowing validation for registration of a new user
    """
    email: EmailField = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    date_of_birth: DateField = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    profile_picture: ImageField = forms.ImageField(required=False)

    class Meta:
        model: SiteUser = SiteUser
        fields = ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_picture')


class LoginForm(AuthenticationForm):
    """
    A form for validating an existing user
    """
    username: CharField = forms.CharField(widget=TextInput())
    password: CharField = forms.CharField(widget=PasswordInput())
