from rest_framework.serializers import ModelSerializer

from apps.catalogos.estado_venta.models import EstadodeVenta

class EstadodeVentaSerializer(ModelSerializer):
    class Meta:
        model = EstadodeVenta
        fields = ['Codigo_EstadoVenta', 'Estado_Venta']