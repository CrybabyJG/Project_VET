from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.catalogos.medicamento.models import Medicamento, DetalleMedicamento


# Register your models here.
@admin.register(Medicamento)
class MedicamentoAdmin(ModelAdmin):
    search_fields = ['Codigo_Medicamento', 'Nombre_Medicamento', 'ID_Presentacion']
    list_display = ['Codigo_Medicamento', 'Nombre_Medicamento', 'ID_Presentacion', 'ID_Unidad_Medida', 'Precio', ]

@admin.register(DetalleMedicamento)
class DetalleMedicamentoAdmin(admin.ModelAdmin):
    search_fields = ['ID_Medicamento', 'ID_Cita']
    list_display = ['ID_Medicamento', 'Cantidad', 'ID_Cita', 'Descripcion', ]