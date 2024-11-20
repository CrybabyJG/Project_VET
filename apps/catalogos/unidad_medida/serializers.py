from rest_framework.serializers import ModelSerializer

from apps.catalogos.unidad_medida.models import UnidadMedida

class UnidadMedidaSerializer(ModelSerializer):
    class Meta:
        model = UnidadMedida
        fields = ['Codigo_Unidad_Medida', 'Nombre_Unidad_Medida']