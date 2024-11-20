from django.db import models

# Create your models here.
class EstadodeCita(models.Model):
    ID_EstadoCita = models.AutoField(primary_key=True)
    Codigo_EstadoCita = models.CharField(max_length=10, verbose_name='Código de estado de cita')
    Estado_Cita = models.CharField(max_length=200, verbose_name='Estado de cita')

    class Meta:
        verbose_name_plural = 'Estados de citas'

    def __str__(self):
        return f'{self.Codigo_EstadoCita} - {self.Estado_Cita}'