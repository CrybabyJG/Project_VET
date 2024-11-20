from rest_framework.serializers import ModelSerializer

from apps.catalogos.mascota.models import Mascota

class MascotaSerializer(ModelSerializer):
    class Meta:
        model = Mascota
        fields = ['Codigo_Mascota', 'Nombre_Mascota', 'Descripcion', 'ID_Raza', 'ID_Cliente']