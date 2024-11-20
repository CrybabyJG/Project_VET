from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Proveedor
from .serializers import ProveedorSerializer
from drf_yasg.utils import swagger_auto_schema

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class ProveedorAPIView(PaginationMixin,APIView):
    """
    Vista para listar todos los proveedores o crear una nueva mascota.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Proveedor

    @swagger_auto_schema(responses={200: ProveedorSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los proveedores.
        """
        logger.info("Peticion GET para listar todas las unidades de medida")
        proveedor = Proveedor.objects.all().order_by('ID_Proveedor')
        page = self.paginate_queryset(proveedor, request)

        if page is not None:
            serializer = ProveedorSerializer(page, many=True)
            logger.info("Respuesta paginada para unidad_medida")
            return self.get_paginated_response(serializer.data)

        serializer = ProveedorSerializer(proveedor, many=True)
        logger.error("Mostrando todas las unidades de medida sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProveedorSerializer, responses={201: ProveedorSerializer()})
    def post(self, request):
        """
        Crear un nuevo proveedor.
        """
        logger.info("Peticicion POST para crear una nuevo proveedor")
        serializer = ProveedorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Proveedor creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el proveedor: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProveedorDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un proveedor específico.
    """

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Proveedor

    @swagger_auto_schema(responses={200: ProveedorSerializer()})
    def get(self, request, pk):
        """
        Obtener un proveedor específico por su ID.
        """
        try:
            proveedor = Proveedor.objects.get(pk=pk)
        except Proveedor.DoesNotExist:
            return Response({'error': 'Proveedor no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProveedorSerializer(proveedor)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProveedorSerializer, responses={200: ProveedorSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un proveedor por su ID.
        """
        logger.info("Solicitud PUT para actualizar el proveedor con ID: %s", pk)
        try:
            proveedor = Proveedor.objects.get(pk=pk)
        except Proveedor.DoesNotExist:
            return Response({'error': 'Proveedor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, proveedor) #Verificación de permisos
        serializer = ProveedorSerializer(proveedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Proveedor actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el proveedor con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProveedorSerializer, responses={200: ProveedorSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un proveedor por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente el proveedor con ID: %s", pk)
        try:
            proveedor = Proveedor.objects.get(pk=pk)
        except Proveedor.DoesNotExist:
            return Response({'error': 'Proveedor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, proveedor) #Verificación de permisos
        serializer = ProveedorSerializer(proveedor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Proveedor parcialmente actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente el proveedor con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un proveedor por su ID.
        """
        logger.info("Solicitud DELETE para eliminar un proveedor con ID: %s", pk)
        try:
            proveedor = Proveedor.objects.get(pk=pk)
        except Proveedor.DoesNotExist:
            return Response({'error': 'Proveedor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, proveedor) #Verificación de permisos
        proveedor.delete()
        logger.info("Proveedor eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)