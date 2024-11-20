from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.presentacion.models import Presentacion


# Register your models here.
@admin.register(Presentacion)
class PresentacionAdmin(ModelAdmin):
    search_fields = ['Codigo_Presentacion', 'Nombre_Presentacion']
    list_display = ['Codigo_Presentacion', 'Nombre_Presentacion']