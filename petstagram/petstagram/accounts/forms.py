from django import forms
from django.contrib.auth import forms as auth_forms

from petstagram.accounts.models import PetstagramUser


class UserEditForm(auth_forms.UserChangeForm):
    class Meta:
        model = PetstagramUser
        fields = '__all__'
        field_classes = {'username': auth_forms.UsernameField}


class PetstagramUserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = PetstagramUser
        fields = ['username', 'email']
        field_classes = {'username': auth_forms.UsernameField}


class PetstagramUserLoginForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(widget=forms.TextInput(attrs={"autofocus": True, 'placeholder': "Username"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'placeholder': "Password"})
    )
