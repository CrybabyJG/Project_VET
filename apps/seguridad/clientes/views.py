from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Clientes
from .serializers import ClientesSerializer
from drf_yasg.utils import swagger_auto_schema

from ..permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class ClientesAPIView(PaginationMixin,APIView):
    """
    Vista para listar todas las razas o crear una nueva raza.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Clientes

    @swagger_auto_schema(responses={200: ClientesSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las razas.
        """
        logger.info("Peticion GET para listar todos los clientes")
        cliente = Clientes.objects.all().order_by('ID_Cliente')
        page = self.paginate_queryset(cliente, request)

        if page is not None:
            serializer = ClientesSerializer(page, many=True)
            logger.info("Respuesta paginada para clientes")
            return self.get_paginated_response(serializer.data)

        serializer = ClientesSerializer(cliente, many=True)
        logger.error("Mostrando todos los clientes sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ClientesSerializer, responses={201: ClientesSerializer()})
    def post(self, request):
        """
        Crear una nueva raza.
        """
        logger.info("Peticicion POST para crear un nuevo cliente")
        serializer = ClientesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Cliente creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el cliente: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientesDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una raza específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Clientes

    @swagger_auto_schema(responses={200: ClientesSerializer()})
    def get(self, request, pk):
        """
        Obtener una raza específica por su ID.
        """
        try:
            cliente = Clientes.objects.get(pk=pk)
        except Clientes.DoesNotExist:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClientesSerializer(cliente)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ClientesSerializer, responses={200: ClientesSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente una raza por su ID.
        """
        logger.info("Solicitud PUT para actualizar el cliente con ID: %s", pk)
        try:
            cliente = Clientes.objects.get(pk=pk)
        except Clientes.DoesNotExist:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, cliente) #Verificación de permisos
        serializer = ClientesSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Cliente actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el cliente con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ClientesSerializer, responses={200: ClientesSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una raza por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente el cliente con ID: %s", pk)
        try:
            cliente = Clientes.objects.get(pk=pk)
        except Clientes.DoesNotExist:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, cliente) #Verificación de permisos
        serializer = ClientesSerializer(cliente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Cliente parcialmente actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente el cliente con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una raza por su ID.
        """
        logger.info("Solicitud DELETE para eliminar un cliente con ID: %s", pk)
        try:
            cliente = Clientes.objects.get(pk=pk)
        except Clientes.DoesNotExist:
            return Response({'error': 'Cliente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, cliente) #Verificación de permisos
        cliente.delete()
        logger.info("Cliente eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)