from django import forms

from .models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('created_date',)
