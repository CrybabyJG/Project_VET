from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.unidad_medida.models import UnidadMedida


# Register your models here.
@admin.register(UnidadMedida)
class UnidadMedidaAdmin(ModelAdmin):
    search_fields = ['Codigo_Unidad_Medida', 'Nombre_Unidad_Medida']
    list_display = ['Codigo_Unidad_Medida', 'Nombre_Unidad_Medida' ]