from rest_framework.serializers import ModelSerializer

from apps.catalogos.estado_compra.models import EstadodeCompra

class EstadodeCompraSerializer(ModelSerializer):
    class Meta:
        model = EstadodeCompra
        fields = ['Codigo_EstadoCompra', 'Estado_Compra']