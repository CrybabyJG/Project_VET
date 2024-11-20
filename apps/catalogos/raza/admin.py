from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.raza.models import Raza


# Register your models here.
@admin.register(Raza)
class RazaAdmin(ModelAdmin):
    search_fields = ['Codigo_Raza', 'Nombre_Raza']
    list_display = ['Codigo_Raza', 'Nombre_Raza', 'ID_TipoMascota']