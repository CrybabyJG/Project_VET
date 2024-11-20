from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.estado_de_cita.models import EstadodeCita


# Register your models here.
@admin.register(EstadodeCita)
class EstadodeCitaAdmin(ModelAdmin):
    search_fields = ['Codigo_EstadoCita', 'Estado_Cita']
    list_display = ['Codigo_EstadoCita', 'Estado_Cita']