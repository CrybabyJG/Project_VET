from django.db import models

# Create your models here.
class EstadodeCompra(models.Model):
    ID_EstadoCompra = models.AutoField(primary_key=True)
    Codigo_EstadoCompra = models.CharField(max_length=10, verbose_name='Código de estado de compra')
    Estado_Compra = models.CharField(max_length=200, verbose_name='Estado de compra')

    class Meta:
        verbose_name_plural = 'Estados de compras'

    def __str__(self):
        return f'{self.Codigo_EstadoCompra} - {self.Estado_Compra}'