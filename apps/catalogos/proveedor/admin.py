from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.proveedor.models import Proveedor


# Register your models here.
@admin.register(Proveedor)
class ProveedorAdmin(ModelAdmin):
    search_fields = ['Codigo_Proveedor', 'Laboratorio']
    list_display = ['Codigo_Proveedor', 'Nombres', 'Apellidos', 'Laboratorio']