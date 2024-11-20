from rest_framework.serializers import ModelSerializer

from apps.catalogos.presentacion.models import Presentacion

class PresentacionSerializer(ModelSerializer):
    class Meta:
        model = Presentacion
        fields = ['Codigo_Presentacion', 'Nombre_Presentacion']