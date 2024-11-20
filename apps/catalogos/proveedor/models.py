from django.db import models

# Create your models here.
class Proveedor(models.Model):
    ID_Proveedor = models.AutoField(primary_key=True)
    Codigo_Proveedor = models.CharField(max_length=10, verbose_name='Código de proveedor', unique=True)
    Nombres = models.CharField(max_length=20, verbose_name='Nombres')
    Apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    Laboratorio = models.CharField(max_length=100, verbose_name='Laboratorio')

    class Meta:
        verbose_name_plural = 'Provedores'

    def __str__(self):
        return f"{self.Codigo_Proveedor} {self.Laboratorio}"