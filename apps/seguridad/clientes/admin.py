from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.seguridad.clientes.models import Clientes


# Register your models here.
@admin.register(Clientes)
class ClienteAdmin(ModelAdmin):
    search_fields = ['Codigo_Cliente', 'Nombres', 'Apellido1', 'Apellido2']
    list_display = ['Codigo_Cliente', 'Nombres', 'Apellido1', 'Apellido2', 'Correo', 'Telefono', 'Direccion']