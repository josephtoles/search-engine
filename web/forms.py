#from django import forms
from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label='url', max_length=100)
