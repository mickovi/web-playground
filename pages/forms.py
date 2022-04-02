from logging import PlaceHolder
from turtle import title
from django import forms
from .models import Page

class PageForm(forms.ModelForm):
    # Usamos una clase Forms para agregar atributos al formulario con los widgets
    class Meta:
        model = Page
        # fields = ['title', 'content', 'order']
        fields = '__all__' # Trae todos los campos en el orden definido en el modelo
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Orden '}),
        }
        labels = {
            'title': '',
            'content': '',
            'order': ''
        }