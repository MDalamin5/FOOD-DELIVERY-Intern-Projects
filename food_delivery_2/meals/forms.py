from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MealOff

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MealOffForm(forms.ModelForm):
    class Meta:
        model = MealOff
        fields = ['date', 'lunch_off', 'dinner_off']
