from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EstadodeCita
from .serializers import EstadodeCitaSerializer
from drf_yasg.utils import swagger_auto_schema

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class EstadodeCitaAPIView(PaginationMixin,APIView):
    """
    Vista para listar todos los estados de citas o crear un nuevo estado de cita.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadodeCita

    @swagger_auto_schema(responses={200: EstadodeCitaSerializer(many=True)})
    def get(self, request):
        """
        Listar todos los estados de citas.
        """
        logger.info("Peticion GET para listar todas los estados de cita")
        estadocita = EstadodeCita.objects.all().order_by('ID_EstadoCita')
        page = self.paginate_queryset(estadocita, request)

        if page is not None:
            serializer = EstadodeCitaSerializer(page, many=True)
            logger.info("Respuesta paginada para estado_cita")
            return self.get_paginated_response(serializer.data)

        serializer = EstadodeCitaSerializer(estadocita, many=True)
        logger.error("Mostrando todas los estados de cita sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EstadodeCitaSerializer, responses={201: EstadodeCitaSerializer()})
    def post(self, request):
        """
        Crear un nuevo estado de cita.
        """
        logger.info("Peticicion POST para crear un nuevo estado de cita")
        serializer = EstadodeCitaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de cita creado exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear el estado de venta: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EstadodeCitaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar un estado de cita específico.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = EstadodeCita

    @swagger_auto_schema(responses={200: EstadodeCitaSerializer()})
    def get(self, request, pk):
        """
        Obtener un estado de cita específico por su ID.
        """
        try:
            estado_cita = EstadodeCita.objects.get(pk=pk)
        except EstadodeCita.DoesNotExist:
            return Response({'error': 'Estado de cita no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EstadodeCitaSerializer(estado_cita)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EstadodeCitaSerializer, responses={200: EstadodeCitaSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente un estado de cita por su ID.
        """
        logger.info("Solicitud PUT para actualizar el estado de cita con ID: %s", pk)
        try:
            estado_cita = EstadodeCita.objects.get(pk=pk)
        except EstadodeCita.DoesNotExist:
            return Response({'error': 'Estado de cita no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estado_cita) #Verificación de permisos
        serializer = EstadodeCitaSerializer(estado_cita, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de cita actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el estado de cita con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=EstadodeCitaSerializer, responses={200: EstadodeCitaSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un estado de cita por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente el estado de cita con ID: %s", pk)
        try:
            estado_cita = EstadodeCita.objects.get(pk=pk)
        except EstadodeCita.DoesNotExist:
            return Response({'error': 'Estado de cita no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estado_cita) #Verificación de permisos
        serializer = EstadodeCitaSerializer(estado_cita, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Estado de cita parcialmente actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente el estado de cita con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un estado de cita por su ID.
        """
        logger.info("Solicitud DELETE para eliminar un estado de cita con ID: %s", pk)
        try:
            estado_cita = EstadodeCita.objects.get(pk=pk)
        except EstadodeCita.DoesNotExist:
            return Response({'error': 'Estado de cita no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, estado_cita) #Verificación de permisos
        estado_cita.delete()
        logger.info("Estado de cita eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)