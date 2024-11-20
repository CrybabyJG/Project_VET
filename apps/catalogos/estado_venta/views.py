from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EstadodeVenta
from .serializers import EstadodeVentaSerializer
from drf_yasg.utils import swagger_auto_schema

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class EstadodeVentaAPIView(PaginationMixin,APIView):
    """
    Vista para listar todos los estados de ventas o crear un nuevo estado de venta.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadodeVenta

    @swagger_auto_schema(responses={200: EstadodeVentaSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los estados de ventas.
        """
        logger.info("Peticion GET para listar todas los estados de venta")
        estadoventa = EstadodeVenta.objects.all().order_by('ID_EstadoVenta')
        page = self.paginate_queryset(estadoventa, request)

        if page is not None:
            serializer = EstadodeVentaSerializer(page, many=True)
            logger.info("Respuesta paginada para estado_venta")
            return self.get_paginated_response(serializer.data)

        serializer = EstadodeVentaSerializer(estadoventa, many=True)
        logger.error("Mostrando todas los estados de venta sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EstadodeVentaSerializer, responses={201: EstadodeVentaSerializer()})
    def post(self, request):
        """
        Crear un nuevo estado de venta.
        """
        logger.info("Peticicion POST para crear un nuevo estado de venta")
        serializer = EstadodeVentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de venta creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el estado de venta: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EstadodeVentaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un estado de venta específico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadodeVenta

    @swagger_auto_schema(responses={200: EstadodeVentaSerializer()})
    def get(self, request, pk):
        """
        Obtener un estado de venta específico por su ID.
        """
        try:
            estado_venta = EstadodeVenta.objects.get(pk=pk)
        except EstadodeVenta.DoesNotExist:
            return Response({'error': 'Estado de venta no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EstadodeVentaSerializer(estado_venta)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EstadodeVentaSerializer, responses={200: EstadodeVentaSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un estado de venta por su ID.
        """
        logger.info("Solicitud PUT para actualizar el estado de venta con ID: %s", pk)
        try:
            estado_venta = EstadodeVenta.objects.get(pk=pk)
        except EstadodeVenta.DoesNotExist:
            return Response({'error': 'Estado de venta no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estado_venta) #Verificación de permisos
        serializer = EstadodeVentaSerializer(estado_venta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de venta actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el estado de venta con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=EstadodeVentaSerializer, responses={200: EstadodeVentaSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un estado de venta por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente el estado de venta con ID: %s", pk)
        try:
            estado_venta = EstadodeVenta.objects.get(pk=pk)
        except EstadodeVenta.DoesNotExist:
            return Response({'error': 'Estado de venta no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estado_venta) #Verificación de permisos
        serializer = EstadodeVentaSerializer(estado_venta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de venta parcialmente actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente el estado de venta con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un estado de venta por su ID.
        """
        logger.info("Solicitud DELETE para eliminar un estado de venta con ID: %s", pk)
        try:
            estado_venta = EstadodeVenta.objects.get(pk=pk)
        except EstadodeVenta.DoesNotExist:
            return Response({'error': 'Estado de venta no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estado_venta) #Verificación de permisos
        estado_venta.delete()
        logger.info("Estado de venta eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)