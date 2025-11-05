from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'dni', 'carrera', 'grado', 'foto', 
                 'telefono', 'telefono_apoderado', 'direccion', 
                 'fecha_inicio', 'dia_pago']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }
