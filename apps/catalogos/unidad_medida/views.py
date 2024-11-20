from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UnidadMedida
from .serializers import UnidadMedidaSerializer
from drf_yasg.utils import swagger_auto_schema
from apps.seguridad.permissions import CustomPermission
from rest_framework.permissions import IsAuthenticated
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class UnidadMedidaAPIView(PaginationMixin,APIView):
    """
    Vista para listar todas las unidades de medida o crear una nueva unidad de medida.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = UnidadMedida

    @swagger_auto_schema(responses={200: UnidadMedidaSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las unidades de medida.
        """
        logger.info("Peticion GET para listar todas las unidades de medida")
        unidad_medida = UnidadMedida.objects.all().order_by('ID_Unidad_Medida')
        page = self.paginate_queryset(unidad_medida, request)

        if page is not None:
            serializer = UnidadMedidaSerializer(page, many=True)
            logger.info("Respuesta paginada para unidad_medida")
            return self.get_paginated_response(serializer.data)

        serializer = UnidadMedidaSerializer(unidad_medida, many=True)
        logger.error("Mostrando todas las unidades de medida sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UnidadMedidaSerializer, responses={201: UnidadMedidaSerializer()})
    def post(self, request):
        """
        Crear una nueva unidad de medida.
        """
        logger.info("Peticicion POST para crear una nueva unidad de medida")
        serializer = UnidadMedidaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Unidad de medida creada exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear la unidad de medida: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnidadMedidaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una unidad de medida específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = UnidadMedida

    @swagger_auto_schema(responses={200: UnidadMedidaSerializer()})
    def get(self, request, pk):
        """
        Obtener una unidad de medida específica por su ID.
        """
        try:
            unidad_medida = UnidadMedida.objects.get(pk=pk)
        except UnidadMedida.DoesNotExist:
            return Response({'error': 'Unidad de medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UnidadMedidaSerializer(unidad_medida)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UnidadMedidaSerializer, responses={200: UnidadMedidaSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente una unidad de medida por su ID.
        """
        logger.info("Solicitud PUT para actualizar la unida de medida con ID: %s", pk)
        try:
            unidad_medida = UnidadMedida.objects.get(pk=pk)
        except UnidadMedida.DoesNotExist:
            return Response({'error': 'Unidad de medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, unidad_medida) #Verificación de permisos
        serializer = UnidadMedidaSerializer(unidad_medida, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Unidad de medida actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar la unidad de medida con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UnidadMedidaSerializer, responses={200: UnidadMedidaSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una unidad de medida por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente la unidad de medida con ID: %s", pk)
        try:
            unidad_medida = UnidadMedida.objects.get(pk=pk)
        except UnidadMedida.DoesNotExist:
            return Response({'error': 'Unidad de medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, unidad_medida) #Verificación de permisos
        serializer = UnidadMedidaSerializer(unidad_medida, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Unidad de medida parcialmente actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente la unidad de medida con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una unidad de medida por su ID.
        """
        logger.info("Solicitud DELETE para eliminar una unidad de medida con ID: %s", pk)
        try:
            unidad_medida = UnidadMedida.objects.get(pk=pk)
        except UnidadMedida.DoesNotExist:
            return Response({'error': 'Unidad de medida no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, unidad_medida) #Verificación de permisos
        unidad_medida.delete()
        logger.info("Unidad de medida eliminada exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)