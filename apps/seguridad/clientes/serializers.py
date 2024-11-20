from rest_framework.serializers import ModelSerializer

from apps.seguridad.clientes.models import Clientes

class ClientesSerializer(ModelSerializer):
    class Meta:
        model = Clientes
        fields = ['Codigo_Cliente', 'Nombres', 'Apellido1', 'Apellido2', 'Correo', 'Telefono', 'Direccion']