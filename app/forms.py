from django import forms
from django.forms import formsets
from .models import Category

class CategoryForm(forms.ModelForm):
   class Meta:
      model = Category
      fields = '__all__'
      widgets = {
         'color': forms.TextInput(attrs={'type': 'color', 'class': ''}),
      }