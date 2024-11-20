from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EstadodeCompra
from .serializers import EstadodeCompraSerializer
from drf_yasg.utils import swagger_auto_schema

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class EstadodeCompraAPIView(PaginationMixin,APIView):
    """
    Vista para listar todos los estados de compras o crear un nuevo estado de compra.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadodeCompra

    @swagger_auto_schema(responses={200: EstadodeCompraSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los estados de compra.
        """
        logger.info("Peticion GET para listar todas los estados de compra")
        estadocompra = EstadodeCompra.objects.all().order_by('ID_EstadoCompra')
        page = self.paginate_queryset(estadocompra, request)

        if page is not None:
            serializer = EstadodeCompraSerializer(page, many=True)
            logger.info("Respuesta paginada para estado_compra")
            return self.get_paginated_response(serializer.data)

        serializer = EstadodeCompraSerializer(estadocompra, many=True)
        logger.error("Mostrando todas los estados de compra sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EstadodeCompraSerializer, responses={201: EstadodeCompraSerializer()})
    def post(self, request):
        """
        Crear un nuevo estado de compra.
        """
        logger.info("Peticicion POST para crear un nuevo estado de compra")
        serializer = EstadodeCompraSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de compra creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el estado de compra: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EstadodeCompraDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un estado de compra específico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadodeCompra

    @swagger_auto_schema(responses={200: EstadodeCompraSerializer()})
    def get(self, request, pk):
        """
        Obtener un estado de compra específico por su ID.
        """
        try:
            estados_compra = EstadodeCompra.objects.get(pk=pk)
        except EstadodeCompra.DoesNotExist:
            return Response({'error': 'Estado de compra no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EstadodeCompraSerializer(estados_compra)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EstadodeCompraSerializer, responses={200: EstadodeCompraSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un estado de compra por su ID.
        """
        logger.info("Solicitud PUT para actualizar el estado de compra con ID: %s", pk)
        try:
            estados_compra = EstadodeCompra.objects.get(pk=pk)
        except EstadodeCompra.DoesNotExist:
            return Response({'error': 'Estado de compra no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estados_compra) #Verificación de permisos
        serializer = EstadodeCompraSerializer(estados_compra, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de compra actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el estado de compra con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=EstadodeCompraSerializer, responses={200: EstadodeCompraSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un estado de compra por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente el estado de compra con ID: %s", pk)
        try:
            estados_compra = EstadodeCompra.objects.get(pk=pk)
        except EstadodeCompra.DoesNotExist:
            return Response({'error': 'Estado de compra no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estados_compra) # Verificación de permisos
        serializer = EstadodeCompraSerializer(estados_compra, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de compraparcialmente actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente el estado de compra con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un estado de compra por su ID.
        """
        logger.info("Solicitud DELETE para eliminar un estado de compra con ID: %s", pk)
        try:
            estados_compra = EstadodeCompra.objects.get(pk=pk)
        except EstadodeCompra.DoesNotExist:
            return Response({'error': 'Estado de compra no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estados_compra) # Verificación de permisos
        estados_compra.delete()
        logger.info("Estado de compra eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)