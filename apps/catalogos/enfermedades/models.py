from django.db import models

# Create your models here.
class Enfermedades(models.Model):
    ID_Enfermedades = models.AutoField(primary_key=True)
    Codigo_Enfermedades = models.CharField(max_length=10, verbose_name='Código de enfermedad', unique=True)
    Nombre_Enfermedad = models.CharField(max_length=200, verbose_name='Nombre de la enfermedad')

    class Meta:
        verbose_name_plural = 'Enfermedades'

    def __str__(self):
        return f'{self.Codigo_Enfermedades} - {self.Nombre_Enfermedad}'