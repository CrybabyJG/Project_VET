from django.db import models

# Create your models here.
class Presentacion(models.Model):
    ID_Presentacion = models.AutoField(primary_key=True)
    Codigo_Presentacion = models.CharField(max_length=10, verbose_name='Código de presentación', unique=True)
    Nombre_Presentacion = models.CharField(max_length=40, verbose_name='Nombre Presentación')

    class Meta:
        verbose_name_plural = 'Presentaciones'

    def __str__(self):
        return f'{self.Codigo_Presentacion} - {self.Nombre_Presentacion}'