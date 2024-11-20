from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField
from .models import Compra, DetalleCompra

class DetalleCompraSerializer(ModelSerializer):
    Nombre_Medicamento = CharField(source='ID_Medicamento.Nombre_Medicamento', read_only=True)
    class Meta:
        model = DetalleCompra
        fields = ['ID_Medicamento', 'Nombre_Medicamento', 'Cantidad']

class CompraSerializer(ModelSerializer):
    Nombre_Proveedor = CharField(source='ID_Proveedor.Laboratorio', read_only=True)
    Nombre_Estado = CharField(source='ID_EstadoCompra.Estado_Compra', read_only=True)
    detalles = DetalleCompraSerializer(many=True)
    class Meta:
        model = Compra
        fields = ['Codigo_Compra', 'ID_Proveedor', 'Nombre_Proveedor', 'Descripcion', 'ID_EstadoCompra','Nombre_Estado', 'detalles']

class UpdateEstadoCompraSerializer(serializers.Serializer):
    ID_EstadoCompra = serializers.IntegerField()