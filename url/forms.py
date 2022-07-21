from email.policy import default
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from url.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class UrlForm(forms.Form):
    long_url=forms.CharField(max_length=255,label='enter your url:')
    

class RegisterForm(forms.ModelForm):
    class Meta:
       model=User
       fields=['username','password']

    def save(self,commit=True,*args,**kwargs):
        self.instance.is_active=True
        self.instance.is_staff=True
        self.instance.password=make_password(self.cleaned_data.get('password'))
        return super().save(commit,*args,**kwargs)

class LoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(max_length=100)
# class LoginForm(AuthenticationForm):
#     username=forms.CharField(max_length=200,label='username')
#     password=forms.CharField(widget=forms.PasswordInput,label='password',max_length=30)

 

      