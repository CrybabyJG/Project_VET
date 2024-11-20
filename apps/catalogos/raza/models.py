from django.db import models
from apps.catalogos.tipo_mascota.models import TipoMascota
# Create your models here.
class Raza(models.Model):
    ID_Raza = models.AutoField(primary_key=True)
    Codigo_Raza = models.CharField(max_length=10, verbose_name='Código de raza', unique=True)
    Nombre_Raza = models.CharField(max_length=200, verbose_name='Raza')
    ID_TipoMascota = models.ForeignKey(TipoMascota, verbose_name='Tipo de Mascota', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Razas'

    def __str__(self):
        return f'{self.Codigo_Raza} {self.Nombre_Raza}'