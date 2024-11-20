from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.mascota.models import Mascota


# Register your models here.
@admin.register(Mascota)
class MascotaAdmin(ModelAdmin):
    search_fields = ['Codigo_Mascota', ]
    list_display = ['Codigo_Mascota', 'Nombre_Mascota', 'Descripcion', 'ID_Raza', 'ID_Cliente']