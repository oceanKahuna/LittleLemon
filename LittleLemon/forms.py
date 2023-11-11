from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django import forms

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

# ModelForm: MenuForm
class MenuForm(forms.Form):
    item_name = forms.CharField(max_length = 200)
    category = forms.CharField(max_length = 200)
    description = forms.CharField(max_length = 1000)
