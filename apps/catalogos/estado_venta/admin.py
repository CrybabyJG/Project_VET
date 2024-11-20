from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.estado_venta.models import EstadodeVenta

# Register your models here.
@admin.register(EstadodeVenta)
class EstadodeVentaAdmin(ModelAdmin):
    search_fields = ['Codigo_EstadoVenta', 'Estado_Venta']
    list_display = ['Codigo_EstadoVenta', 'Estado_Venta']