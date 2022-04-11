from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=500, required=False)
    profession = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'profession']
