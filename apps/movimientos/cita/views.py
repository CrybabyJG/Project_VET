from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CitaSerializer, DetalleCitaSerializer, UpdateEstadoCitaSerializer
from .models import Cita, Detalle_Cita, Mascota, EstadodeCita, Enfermedades
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class CitaAPIView(PaginationMixin,APIView):

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Cita

    @swagger_auto_schema(responses={200: CitaSerializer()})
    def get(self, request):
        logger.info("Peticion GET para listar todas las citas")
        cita = Cita.objects.all().order_by('ID_Cita')
        page = self.paginate_queryset(cita, request)

        if page is not None:
            serializer = CitaSerializer(page, many=True)
            logger.info("Respuesta paginada para cita")
            return self.get_paginated_response(serializer.data)

        serializer = CitaSerializer(cita, many=True)
        logger.error("Mostrando todas las citas sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CitaSerializer)
    def post(self, request):
        logger.info("Peticicion POST para crear una nueva cita")
        serializer = CitaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Crea la instancia de Cita con los datos validados
                    estado_cita = get_object_or_404(EstadodeCita,
                                                    pk=serializer.validated_data['ID_EstadoCita'].ID_EstadoCita)
                    mascota = get_object_or_404(Mascota, pk=serializer.validated_data['ID_Mascota'].ID_Mascota)

                    cita = Cita.objects.create(
                        Codigo_Cita=serializer.validated_data['Codigo_Cita'],
                        Fecha_de_Cita=serializer.validated_data['Fecha_de_Cita'],
                        Peso=serializer.validated_data['Peso'],
                        ID_EstadoCita=estado_cita,
                        ID_Mascota=mascota
                    )
                    # Procesa cada detalle en los datos validados
                    for detalle_data in serializer.validated_data['detalles']:
                        enfermedad = get_object_or_404(Enfermedades, pk=detalle_data['ID_Enfermedades'].ID_Enfermedades)
                        Detalle_Cita.objects.create(
                            Codigo_DetalleCita=detalle_data['Codigo_DetalleCita'],
                            Descripcion=detalle_data['Descripcion'],
                            ID_Enfermedades=enfermedad,
                            ID_Cita=cita
                        )
                cita_serializer = CitaSerializer(cita)
                logger.info("Cita creada exitosamente")
                return Response(cita_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error("No se pudo crear la cita: %s", serializer.errors)
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CitaDetails(APIView):

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Cita

    @swagger_auto_schema(responses={200: CitaSerializer()})
    def get(self, request, pk):
        # Obtiene la cita por ID
        cita = get_object_or_404(Cita, pk=pk)
        serializer = CitaSerializer(cita)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CitaEstadoUpdateAPIView(APIView):

    @swagger_auto_schema(
        request_body=UpdateEstadoCitaSerializer,
        responses={200: "Estado de cita actualizado con éxito.", 404: "Cita o EstadoCita no encontrado.",
                    400: "Datos inválidos."}
    )
    def patch(self, request, pk):
        logger.info("Solicitud PATCH para actualizar parcialmente el estado de la cita ID: %s", pk)
        serializer = UpdateEstadoCitaSerializer(data=request.data)
        if serializer.is_valid():
            cita = get_object_or_404(Cita, pk=pk)
            estado_cita = get_object_or_404(EstadodeCita, pk=serializer.validated_data['ID_EstadoCita'])
            cita.ID_EstadoCompra = estado_cita
            cita.save()
            logger.info("Estado de cita parcialmente actualizado exitosamente con ID: %s", pk)
            return Response({"message": "Estado de cita actualizado con éxito."}, status=status.HTTP_200_OK)
        logger.error("No se pudo actualizar el estado de la cita: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    def delete(self, request, pk=None):
        cita = get_object_or_404(Cita, pk=pk)
        try:
            with transaction.atomic():
                #self.check_object_permissions(request, cita) #Verificación de permisos
                # Elimina primero los detalles relacionados con la cita
                Detalle_Cita.objects.filter(ID_Cita=cita).delete()
                # Luego, elimina la cita
                cita.delete()

            return Response({"message": "Cita eliminada con éxito."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    """