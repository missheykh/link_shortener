from django import forms

class UrlForm(forms.Form):
    long_url=forms.CharField(max_length=255,label='enter your url:')
    

