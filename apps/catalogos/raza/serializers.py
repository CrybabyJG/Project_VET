from rest_framework.serializers import ModelSerializer

from apps.catalogos.raza.models import Raza

class RazaSerializer(ModelSerializer):
    class Meta:
        model = Raza
        fields = ['Codigo_Raza', 'Nombre_Raza', 'ID_TipoMascota']