from django import forms


# Form used to inpur just a URL
class URLForm(forms.Form):
    url = forms.URLField(label='url', max_length=100)


# Form used to create a form model
class SearchForm(forms.Form):
    title = forms.CharField(max_length=100)
    url = forms.URLField(label='url', max_length=100)


# Form used to login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)
