from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.enfermedades.models import Enfermedades


# Register your models here.
@admin.register(Enfermedades)
class EnfermedadesAdmin(ModelAdmin):
    search_fields = ['Codigo_Enfermedades', 'Nombre_Enfermedad']
    list_display = ['Codigo_Enfermedades', 'Nombre_Enfermedad']