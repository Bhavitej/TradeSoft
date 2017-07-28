from django import forms
from django.contrib.auth.models import User

from .models import Company


class CompanyForm(forms.ModelForm):

    class Meta:
        model =  Company
        fields = ['company_name', 'company_stock_code', 'company_logo']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
