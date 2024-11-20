from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Presentacion
from .serializers import PresentacionSerializer
from drf_yasg.utils import swagger_auto_schema

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class PresentacionAPIView(PaginationMixin,APIView):
    """
    Vista para listar todas las presentaciones o crear una nueva presentación.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Presentacion

    @swagger_auto_schema(responses={200: PresentacionSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las presentaciones.
        """
        logger.info("Peticion GET para listar todas las presentaciones")
        presentacion = Presentacion.objects.all().order_by('ID_Presentacion')
        page = self.paginate_queryset(presentacion, request)

        if page is not None:
            serializer = PresentacionSerializer(page, many=True)
            logger.info("Respuesta paginada para presentacion")
            return self.get_paginated_response(serializer.data)

        serializer = PresentacionSerializer(presentacion, many=True)
        logger.error("Mostrando todas las presentaciones sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PresentacionSerializer, responses={201: PresentacionSerializer()})
    def post(self, request):
        """
        Crear una nueva presentación.
        """
        logger.info("Peticicion POST para crear una nueva presentacion")
        serializer = PresentacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Presentacion creada exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear la presentacion: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PresentacionDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una presentación específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Presentacion

    @swagger_auto_schema(responses={200: PresentacionSerializer()})
    def get(self, request, pk):
        """
        Obtener una presentación específica por su ID.
        """
        try:
            presentacion = Presentacion.objects.get(pk=pk)
        except Presentacion.DoesNotExist:
            return Response({'error': 'Presentación no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PresentacionSerializer(presentacion)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PresentacionSerializer, responses={200: PresentacionSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente una presentación por su ID.
        """
        logger.info("Solicitud PUT para actualizar la presentacion con ID: %s", pk)
        try:
            presentacion = Presentacion.objects.get(pk=pk)
        except Presentacion.DoesNotExist:
            return Response({'error': 'Presentación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, presentacion) #Verificación de permisos
        serializer = PresentacionSerializer(presentacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Presentacion actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar la presentacion con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PresentacionSerializer, responses={200: PresentacionSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una presentación por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente la presentacion con ID: %s", pk)
        try:
            presentacion = Presentacion.objects.get(pk=pk)
        except Presentacion.DoesNotExist:
            return Response({'error': 'Presentación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, presentacion) #Verificación de permisos
        serializer = PresentacionSerializer(presentacion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Presentacion parcialmente actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente la presentacion con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una presentación por su ID.
        """
        logger.info("Solicitud DELETE para eliminar una presentacion con ID: %s", pk)
        try:
            presentacion = Presentacion.objects.get(pk=pk)
        except Presentacion.DoesNotExist:
            return Response({'error': 'Presentación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, presentacion) #Verificación de permisos
        presentacion.delete()
        logger.info("Presentacion eliminada exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)