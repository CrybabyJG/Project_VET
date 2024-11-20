from django.db import models
from apps.catalogos.estado_de_cita.models import EstadodeCita
from apps.catalogos.mascota.models import Mascota
from apps.catalogos.enfermedades.models import Enfermedades
# Create your models here.
class Cita(models.Model):
    ID_Cita = models.AutoField(primary_key=True)
    Codigo_Cita = models.CharField(max_length=10, verbose_name='Código Cita', unique=True)
    Fecha_Realizacion = models.DateField(verbose_name='Fecha de realización', auto_now_add=True)
    Fecha_de_Cita = models.DateField(verbose_name='Fecha para cita')
    Peso = models.CharField(max_length=30, verbose_name='Peso')
    ID_EstadoCita = models.ForeignKey(EstadodeCita, verbose_name='Estado de la cita',on_delete=models.PROTECT)
    ID_Mascota = models.ForeignKey(Mascota, verbose_name='Mascota',on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Citas'

    def __str__(self):
        return f'{self.Codigo_Cita} - {self.Fecha_Realizacion}'


class Detalle_Cita(models.Model):
    ID_DetalleCita = models.AutoField(primary_key=True)
    Codigo_DetalleCita = models.CharField(max_length=10, verbose_name='Código de detalle cita', unique=True)
    Descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    ID_Enfermedades = models.ForeignKey(Enfermedades, verbose_name='Enfermedad', on_delete=models.PROTECT)
    ID_Cita = models.ForeignKey(Cita, related_name='detalles', verbose_name='Cita No', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Detalles de Citas'

    def __str__(self):
        return f'{self.Codigo_DetalleCita} - {self.ID_Cita.Codigo_Cita} - {self.ID_Enfermedades}'