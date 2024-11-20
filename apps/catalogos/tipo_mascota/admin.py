from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.tipo_mascota.models import TipoMascota


# Register your models here.
@admin.register(TipoMascota)
class TipoMascotaAdmin(ModelAdmin):
    search_fields = ['Codigo_TipoMascota', 'Nombre_TipoMascota']
    list_display = ['Codigo_TipoMascota', 'Nombre_TipoMascota']