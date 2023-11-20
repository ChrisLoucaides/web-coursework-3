from django import forms
from django.contrib.auth.forms import UserCreationForm

from api.models import SiteUser


class SignupForm(UserCreationForm):
    class Meta:
        model = SiteUser
        fields = ['email', 'date_of_birth']
