from django import forms
from django.contrib.auth.models import User

class Loginform(forms.Form):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username_login',
                                                                            'class': 'form-control',
                                                                            'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password_login',
                                                                 'class': 'form-control', 'placeholder': 'Password'}))


class Signupform(forms.Form):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_pass')

    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'username',
                                                                            'class': 'form-control',
                                                                            'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'first_name',
                                                                              'class': 'form-control',
                                                                              'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'last_name',
                                                                             'class': 'form-control',
                                                                             'placeholder': 'Last name'}))
    email = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'id': 'email',
                                                                         'class': 'form-control',
                                                                         'placeholder': 'somone@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password',
                                                                 'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password',
                                                                         'class': 'form-control',
                                                                         'placeholder': 'Confirm Password'}))
