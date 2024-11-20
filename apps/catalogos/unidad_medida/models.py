from django.db import models

# Create your models here.
class UnidadMedida(models.Model):
    ID_Unidad_Medida = models.AutoField(primary_key=True)
    Codigo_Unidad_Medida = models.CharField(max_length=10, verbose_name='Código de unidad medida', unique=True)
    Nombre_Unidad_Medida = models.CharField(max_length=40, verbose_name='Nombre de la unidad de medida')

    class Meta:
        verbose_name_plural = 'Unidades de Medidas'

    def __str__(self):
        return f'{self.Codigo_Unidad_Medida} - {self.Nombre_Unidad_Medida}'