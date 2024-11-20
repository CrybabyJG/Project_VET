from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.movimientos.compra.models import Compra, DetalleCompra


# Register your models here.
@admin.register(Compra)
class CompraAdmin(ModelAdmin):
    search_fields = ['Codigo_Compra', 'Descripcion', 'Fecha']
    list_display = ['Codigo_Compra', 'Descripcion', 'Fecha', 'ID_Proveedor', 'ID_EstadoCompra']

@admin.register(DetalleCompra)
class DetalleVentaAdmin(ModelAdmin):
    search_fields = ['ID_Compra', 'ID_Medicamento']
    list_display = ['ID_Compra', 'ID_Medicamento', 'Cantidad', 'Precio']