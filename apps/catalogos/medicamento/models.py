from django.db import models
from apps.catalogos.presentacion.models import Presentacion
from apps.catalogos.unidad_medida.models import UnidadMedida
from apps.movimientos.cita.models import Cita


# Create your models here.
class Medicamento(models.Model):
    ID_Medicamento = models.AutoField(primary_key=True)
    Codigo_Medicamento = models.CharField(max_length=10, verbose_name='Código de medicamento', unique=True)
    Nombre_Medicamento = models.CharField(max_length=200, verbose_name='Nombre del Medicamento')
    Precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    ID_Presentacion = models.ForeignKey(Presentacion, verbose_name='Presentación del medicamento', on_delete=models.PROTECT)
    ID_Unidad_Medida = models.ForeignKey(UnidadMedida, verbose_name='Unidad de medida', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Medicamentos'

    def __str__(self):
        return f'{self.Codigo_Medicamento} - {self.Nombre_Medicamento}'

class DetalleMedicamento(models.Model):
    ID_DetalleEnfermedades = models.AutoField(primary_key=True)
    Cantidad = models.IntegerField(verbose_name='Cantidad')
    Descripcion = models.CharField(max_length=300, verbose_name='Descripcion')
    ID_Cita = models.ForeignKey(Cita, verbose_name='Cita No.', on_delete=models.PROTECT)
    ID_Medicamento = models.ForeignKey(Medicamento, related_name='detalles', verbose_name = 'Medicamento', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Detalles Medicamentos'