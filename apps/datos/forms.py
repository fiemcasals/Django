"""
==============================================================================
apps/datos/forms.py - Formularios para Gestión de Ítems / Recursos
==============================================================================
"""

from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    """
    Formulario basado en modelo (ModelForm) con validaciones personalizadas.
    """

    class Meta:
        model = Item
        fields = ['titulo', 'categoria', 'descripcion', 'precio', 'disponible']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Curso de Python'}),
            'categoria': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Programación'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Descripción detallada...'}),
            'precio': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if len(titulo) < 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return titulo

    def clean_precio(self):
        precio = self.cleaned_data.get('precio', 0.0)
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser un número negativo.")
        return precio
