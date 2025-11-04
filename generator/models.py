from django.db import models

from django.db import models

class Estudiante(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    grado = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.dni})"

