from django.contrib.auth.forms import UserCreationForm
from django import forms
class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text= None
            self.fields[fieldname].widget.attrs.update({'class':'form-control'})


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
