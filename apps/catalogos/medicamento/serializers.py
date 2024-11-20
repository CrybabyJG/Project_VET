from rest_framework.serializers import ModelSerializer, CharField
from .models import Medicamento, DetalleMedicamento

class DetalleMedicamentoSerializer(ModelSerializer):
    Codigo_Cita = CharField(source='ID_Cita.Codigo_Cita', read_only=True)
    class Meta:
        model = DetalleMedicamento
        fields = ['ID_Cita', 'Codigo_Cita', 'Cantidad', 'Descripcion']

class MedicamentoSerializer(ModelSerializer):
    Presentacion = CharField(source='ID_Presentacion.Peso', read_only=True)
    Unidad_de_Medida = CharField(source='ID_Unidad_Medida.Descripcion', read_only=True)
    detalles = DetalleMedicamentoSerializer(many=True)
    class Meta:
        model = Medicamento
        fields = ['Codigo_Medicamento', 'Nombre_Medicamento', 'Precio', 'ID_Presentacion', 'Presentacion', 'ID_Unidad_Medida',
                  'Unidad_de_Medida', 'detalles']