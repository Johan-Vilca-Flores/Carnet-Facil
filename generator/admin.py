from django.contrib import admin
from .models import Estudiante
# Register your models here.
@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'carrera', 'grado')  # columnas visibles
    search_fields = ('nombre', 'dni')  