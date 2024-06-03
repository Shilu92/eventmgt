from django import forms

from .models import UserRegistration


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = ['username', 'email','password','created_at']