from django import forms
from django.contrib.auth import forms as auth_forms

class LoginForm(auth_forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
        self.fields['password'].widget.attrs['placeholder'] = 'パスワード'

