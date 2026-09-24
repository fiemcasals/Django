"""
==============================================================================
apps/core/forms.py - Formularios en Django
==============================================================================
Explicación para alumnos:
En Django, los 'Formularios' se encargan de:
1. Renderizar campos HTML (inputs, textareas, selects, checkboxes).
2. Validar que los datos enviados por el usuario sean seguros y correctos.
3. Convertir el texto recibido en tipos de Python (int, date, boolean).

Tipos de formularios:
- 'forms.Form': Formulario estándar independiente de la base de datos.
- 'forms.ModelForm': Formulario vinculado directamente a un Modelo (crea o edita registros automáticamente).
==============================================================================
"""

from django import forms
from .models import MensajeBienvenida


class MensajeBienvenidaForm(forms.ModelForm):
    """
    Formulario vinculado al modelo MensajeBienvenida.
    Genera automáticamente los inputs HTML correspondientes a los campos del modelo.
    """
    class Meta:
        model = MensajeBienvenida
        fields = ['titulo', 'contenido', 'activo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresá el título del mensaje...',
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribí el contenido explicativo...',
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_titulo(self):
        """
        Ejemplo de validación personalizada para un campo específico:
        El método debe llamarse 'clean_<nombre_campo>()'.
        """
        titulo = self.cleaned_data.get('titulo')
        if len(titulo.strip()) < 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return titulo.strip()
