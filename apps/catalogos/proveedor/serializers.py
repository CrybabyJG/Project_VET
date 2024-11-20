from rest_framework.serializers import ModelSerializer

from apps.catalogos.proveedor.models import Proveedor

class ProveedorSerializer(ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['Codigo_Proveedor', 'Nombres', 'Apellidos', 'Laboratorio']