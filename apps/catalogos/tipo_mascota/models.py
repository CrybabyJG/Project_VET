from django.db import models

# Create your models here.
class TipoMascota(models.Model):
    ID_TipoMascota = models.AutoField(primary_key=True)
    Codigo_TipoMascota = models.CharField(max_length=10, verbose_name='Código de tipo mascota', unique=True)
    Nombre_TipoMascota = models.CharField(max_length=200, verbose_name='Tipo de mascota')

    class Meta:
        verbose_name_plural = 'Tipos de mascotas'

    def __str__(self):
        return f'{self.Codigo_TipoMascota} - {self.Nombre_TipoMascota}'