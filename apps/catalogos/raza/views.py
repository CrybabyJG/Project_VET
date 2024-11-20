from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Raza
from .serializers import RazaSerializer
from drf_yasg.utils import swagger_auto_schema

from ...seguridad.permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

class RazaAPIView(PaginationMixin,APIView):
    """
    Vista para listar todas las razas o crear una nueva raza.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Raza

    @swagger_auto_schema(responses={200: RazaSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las razas.
        """
        logger.info("Peticion GET para listar todas las razas")
        razas = Raza.objects.all().order_by('ID_Raza')
        page = self.paginate_queryset(razas, request)

        if page is not None:
            serializer = RazaSerializer(page, many=True)
            logger.info("Respuesta paginada para raza")
            return self.get_paginated_response(serializer.data)

        serializer = RazaSerializer(razas, many=True)
        logger.error("Mostrando todas las razas sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=RazaSerializer, responses={201: RazaSerializer()})
    def post(self, request):
        """
        Crear una nueva raza.
        """
        logger.info("Peticicion POST para crear una nueva raza")
        serializer = RazaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Raza creada exitosamente")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("No se pudo crear la raza: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RazaDetails(APIView):
    """
    Vista para obtener, actualizar o eliminar una raza específica.
    """
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Raza

    @swagger_auto_schema(responses={200: RazaSerializer()})
    def get(self, request, pk):
        """
        Obtener una raza específica por su ID.
        """
        try:
            raza = Raza.objects.get(pk=pk)
        except Raza.DoesNotExist:
            return Response({'error': 'Raza no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RazaSerializer(raza)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=RazaSerializer, responses={200: RazaSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente una raza por su ID.
        """
        logger.info("Solicitud PUT para actualizar la raza con ID: %s", pk)
        try:
            raza = Raza.objects.get(pk=pk)
        except Raza.DoesNotExist:
            return Response({'error': 'Raza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, raza) #Verificación de permisos
        serializer = RazaSerializer(raza, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Raza actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar la raza con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=RazaSerializer, responses={200: RazaSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente una raza por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente la raza con ID: %s", pk)
        try:
            raza = Raza.objects.get(pk=pk)
        except Raza.DoesNotExist:
            return Response({'error': 'Raza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, raza) #Verificación de permisos
        serializer = RazaSerializer(raza, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Raza parcialmente actualizada exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente la raza con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar una raza por su ID.
        """
        logger.info("Solicitud DELETE para eliminar una raza con ID: %s", pk)
        try:
            raza = Raza.objects.get(pk=pk)
        except Raza.DoesNotExist:
            return Response({'error': 'Raza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, raza) #Verificación de permisos
        raza.delete()
        logger.info("Raza eliminada exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)