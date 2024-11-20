from rest_framework.serializers import ModelSerializer

from apps.catalogos.estado_de_cita.models import EstadodeCita

class EstadodeCitaSerializer(ModelSerializer):
    class Meta:
        model = EstadodeCita
        fields = ['Codigo_EstadoCita', 'Estado_Cita']