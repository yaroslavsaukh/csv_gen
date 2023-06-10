from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Password'})
    )


class SchemaForm(forms.ModelForm):
    class Meta:
        model = SchemaModel
        fields = ['name', 'column_sep', 'string_character']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'column_sep': forms.Select(attrs={'class': 'form-select'}),
            'string_character': forms.Select(attrs={'class': 'form-select'})
        }


class ColumnsForm(forms.ModelForm):
    class Meta:
        model = SchemaColumn
        fields = ['name', 'data_type', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'data_type': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.TextInput(attrs={'class': 'form-control'})
        }


class GenerateFile(forms.Form):
    rows = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rows'}))


ColumnFormSet = inlineformset_factory(
    SchemaModel, SchemaColumn, form=ColumnsForm, extra=0, can_delete=True, can_delete_extra=True
)
