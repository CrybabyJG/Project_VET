from rest_framework.serializers import ModelSerializer

from apps.catalogos.tipo_mascota.models import TipoMascota

class TipoMascotaSerializer(ModelSerializer):
    class Meta:
        model = TipoMascota
        fields = ['Codigo_TipoMascota', 'Nombre_TipoMascota']