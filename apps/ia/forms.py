"""
==============================================================================
apps/ia/forms.py - Formularios de Consulta para Inteligencia Artificial
==============================================================================
Explicación para alumnos:
En Django, los Formularios ('forms.Form') se encargan de:
1. Generar los campos HTML correspondientes (<input>, <textarea>).
2. Validar que los datos enviados por el usuario sean seguros y válidos (is_valid()).
3. Prevenir inyecciones y ataques XSS sanitizando el texto recibido.
==============================================================================
"""

from django import forms


class ConsultaIAForm(forms.Form):
    """
    Formulario para recibir preguntas en lenguaje natural y enviarlas al
    servicio de IA Claude con Tool Calling en 2 Fases.
    """
    pregunta = forms.CharField(
        label="Escribe tu consulta",
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ej: ¿Qué tutoriales sobre Django o PostgreSQL tienen disponibles?',
                'autocomplete': 'off',
                'id': 'id_pregunta_ia'
            }
        ),
        help_text="Haz una pregunta en lenguaje natural. Claude elegirá la herramienta adecuada para consultar PostgreSQL."
    )

    def clean_pregunta(self):
        """
        Validación y sanitización personalizada del texto de la pregunta.
        """
        pregunta = self.cleaned_data.get('pregunta', '').strip()
        if len(pregunta) < 3:
            raise forms.ValidationError("La consulta debe tener al menos 3 caracteres.")
        return pregunta
