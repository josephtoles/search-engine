#from django import forms
from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label='url', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
