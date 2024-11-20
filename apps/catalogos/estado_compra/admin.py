from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.estado_compra.models import EstadodeCompra

# Register your models here.
@admin.register(EstadodeCompra)
class EstadodeCompraAdmin(ModelAdmin):
    search_fields = ['Codigo_EstadoCompra', 'Estado_Compra']
    list_display = ['Codigo_EstadoCompra', 'Estado_Compra']