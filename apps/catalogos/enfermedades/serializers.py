from rest_framework.serializers import ModelSerializer

from apps.catalogos.enfermedades.models import Enfermedades

class EnfermedadesSerializer(ModelSerializer):
    class Meta:
        model = Enfermedades
        fields = ['Codigo_Enfermedades', 'Nombre_Enfermedad']