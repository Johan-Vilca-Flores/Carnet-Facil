from django.db import models
from django.utils import timezone
from django.db import models

class Estudiante(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    grado = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos/', blank=True, null=True)
    telefono = models.CharField(
        max_length=9, 
        verbose_name="Teléfono del Estudiante",
        default="000000000"
    )
    telefono_apoderado = models.CharField(
        max_length=9, 
        verbose_name="Teléfono del Apoderado",
        default="000000000"
    )
    direccion = models.CharField(
        max_length=200, 
        verbose_name="Dirección",
        default="Sin dirección"
    )
    fecha_inicio = models.DateField(
        verbose_name="Fecha de Inicio",
        default=timezone.now
    )
    dia_pago = models.IntegerField(
        verbose_name="Día de Pago", 
        choices=[(i,i) for i in range(1,32)],
        default=1
    )
    def __str__(self):
        return f"{self.nombre} ({self.dni})"

