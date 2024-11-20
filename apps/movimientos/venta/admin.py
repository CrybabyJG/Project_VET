from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.movimientos.venta.models import Venta, DetalleVenta


# Register your models here.
@admin.register(Venta)
class VentaAdmin(ModelAdmin):
    search_fields = ['Codigo_Venta', 'Fecha', 'ID_Cliente']
    list_display = ['Codigo_Venta', 'ID_Cliente', 'Descripcion', 'Fecha', 'ID_EstadoVenta']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(ModelAdmin):
    search_fields = ['ID_Venta', 'ID_Medicamento']
    list_display = ['Cantidad', 'Precio', 'ID_Venta', 'ID_Medicamento']