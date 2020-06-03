from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField();
    
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'input100',
        }
    ))

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input100',
        }
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input100',
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'input100',
        }
    ))
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email', 'password1', 'password2', 'is_active']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user