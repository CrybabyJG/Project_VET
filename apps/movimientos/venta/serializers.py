from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField
from .models import Venta, DetalleVenta

class DetalleVentaSerializer(ModelSerializer):
    Nombre_Medicamento = CharField(source='ID_Medicamento.Nombre_Medicamento', read_only=True)
    class Meta:
        model = DetalleVenta
        fields = ['ID_Medicamento', 'Nombre_Medicamento', 'Cantidad']

class VentaSerializer(ModelSerializer):
    Nombre_Cliente = CharField(source='ID_Cliente.Nombres', read_only=True)
    Nombre_Estado = CharField(source='ID_EstadoVenta.Estado_Venta', read_only=True)
    detalles = DetalleVentaSerializer(many=True)
    class Meta:
        model = Venta
        fields = ['Codigo_Venta', 'ID_Cliente', 'Nombre_Cliente', 'Descripcion','ID_EstadoVenta', 'Nombre_Estado', 'detalles']

class UpdateEstadoVentaSerializer(serializers.Serializer):
    ID_EstadoVenta = serializers.IntegerField()