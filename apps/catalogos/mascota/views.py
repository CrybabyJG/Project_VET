from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogos.mascota.models import Mascota
from .serializers import MascotaSerializer
from drf_yasg.utils import swagger_auto_schema

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.
class MascotaAPIView(PaginationMixin,APIView):
    """
    Vista para listar todas las mascotas o crear una nueva mascota.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Mascota

    @swagger_auto_schema(responses={200: MascotaSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las mascotas.
        """
        logger.info("Peticion GET para listar todas las mascotas")
        mascota = Mascota.objects.all().order_by('ID_Mascota')
        page = self.paginate_queryset(mascota, request)

        if page is not None:
            serializer = MascotaSerializer(page, many=True)
            logger.info("Respuesta paginada para mascota")
            return self.get_paginated_response(serializer.data)

        serializer = MascotaSerializer(mascota, many=True)
        logger.error("Mostrando todas las mascotas sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MascotaSerializer, responses={201: MascotaSerializer()})
    def post(self, request):
        """
        Crear una nueva mascota.
        """
        logger.info("Peticicion POST para crear una nueva mascota")
        serializer = MascotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Mascota creada exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear la mascota: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MascotaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una mascota específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Mascota

    @swagger_auto_schema(responses={200: MascotaSerializer()})
    def get(self, request, pk):
        """
        Obtener una mascota específica por su ID.
        """
        try:
            mascota = Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            return Response({'error': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MascotaSerializer(mascota)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MascotaSerializer, responses={200: MascotaSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente una mascota por su ID.
        """
        logger.info("Solicitud PUT para actualizar la mascota con ID: %s", pk)
        try:
            mascota = Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            return Response({'error': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, mascota) #Verificación de permisos
        serializer = MascotaSerializer(mascota, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Mascota actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar la mascota con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=MascotaSerializer, responses={200: MascotaSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una mascota por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente la mascota con ID: %s", pk)
        try:
            mascota = Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            return Response({'error': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, mascota) #Verificación de permisos
        serializer = MascotaSerializer(mascota, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Mascota parcialmente actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente la mascota con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una mascota por su ID.
        """
        logger.info("Solicitud DELETE para eliminar una mascota con ID: %s", pk)
        try:
            mascota = Mascota.objects.get(pk=pk)
        except Mascota.DoesNotExist:
            return Response({'error': 'Mascota no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, mascota) #Verificación de permisos
        mascota.delete()
        logger.info("Mascota eliminada exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)