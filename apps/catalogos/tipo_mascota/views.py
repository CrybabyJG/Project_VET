from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TipoMascota
from .serializers import TipoMascotaSerializer
from drf_yasg.utils import swagger_auto_schema

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)


class TipoMascotaAPIView(PaginationMixin,APIView):
    """
    Vista para listar todos los tipos de mascota o crear un nuevo tipo de mascota.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TipoMascota

    @swagger_auto_schema(responses={200: TipoMascotaSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los tipos de mascota.
        """
        logger.info("Peticion GET para listar todos los tipo de mascotas")
        tipomascota = TipoMascota.objects.all().order_by('ID_TipoMascota')
        page = self.paginate_queryset(tipomascota, request)

        if page is not None:
            serializer = TipoMascotaSerializer(page, many=True)
            logger.info("Respuesta paginada para tipo_mascota")
            return self.get_paginated_response(serializer.data)

        serializer = TipoMascotaSerializer(tipomascota, many=True)
        logger.error("Mostrando todos los tipos de mascotas sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TipoMascotaSerializer, responses={201: TipoMascotaSerializer()})
    def post(self, request):
        """
        Crear un nuevo tipo de mascota.
        """
        logger.info("Peticicion POST para crear un nuevo tipo de mascota")
        serializer = TipoMascotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo de mascota creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el tipo de mascota: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TipoMascotaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un tipo de mascota específico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = TipoMascota

    @swagger_auto_schema(responses={200: TipoMascotaSerializer()})
    def get(self, request, pk):
        """
        Obtener un tipo de mascota específico por su ID.
        """
        try:
            tipo_mascota = TipoMascota.objects.get(pk=pk)
        except TipoMascota.DoesNotExist:
            return Response({'error': 'Tipo de mascota no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TipoMascotaSerializer(tipo_mascota)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TipoMascotaSerializer, responses={200: TipoMascotaSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un tipo de mascota por su ID.
        """
        logger.info("Solicitud PUT para actualizar el tipo de mascota con ID: %s", pk)
        try:
            tipo_mascota = TipoMascota.objects.get(pk=pk)
        except TipoMascota.DoesNotExist:
            return Response({'error': 'Tipo de mascota no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, tipo_mascota) #Verificación de permisos
        serializer = TipoMascotaSerializer(tipo_mascota, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo de mascota actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el tipo de mascota con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TipoMascotaSerializer, responses={200: TipoMascotaSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un tipo de mascota por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente el tipo de mascota con ID: %s", pk)
        try:
            tipo_mascota = TipoMascota.objects.get(pk=pk)
        except TipoMascota.DoesNotExist:
            return Response({'error': 'Tipo de mascota no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, tipo_mascota) #Verificación de permisos
        serializer = TipoMascotaSerializer(tipo_mascota, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Tipo de mascota parcialmente actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente el tipo de mascota con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un tipo de mascota por su ID.
        """
        logger.info("Solicitud DELETE para eliminar un tipo de mascota con ID: %s", pk)
        try:
            tipo_mascota = TipoMascota.objects.get(pk=pk)
        except TipoMascota.DoesNotExist:
            return Response({'error': 'Tipo de mascota no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, tipo_mascota) #Verificación de permisos
        tipo_mascota.delete()
        logger.info("Tipo de mascota eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)