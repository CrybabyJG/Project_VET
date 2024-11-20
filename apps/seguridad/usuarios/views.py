from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuarios
from .serializers import UsuariosSerializer
from drf_yasg.utils import swagger_auto_schema
from ..permissions import CustomPermission
from config.utils.Pagination import PaginationMixin
import logging.handlers

logger = logging.getLogger(__name__)

# Create your views here.
class UsuariosAPIView(PaginationMixin,APIView):

    permission_classes = [IsAuthenticated, CustomPermission]
    model = Usuarios

    @swagger_auto_schema(responses={200: UsuariosSerializer(many=True)})
    def get(self, request):
        """
        Listar todas las unidades de medida.
        """
        logger.info("Peticion GET para listar todos los usuarios")
        usuarios = Usuarios.objects.all().order_by('id')
        page = self.paginate_queryset(usuarios, request)

        if page is not None:
            serializer = UsuariosSerializer(page, many=True)
            logger.info("Respuesta paginada para usuarios")
            return self.get_paginated_response(serializer.data)

        serializer = UsuariosSerializer(usuarios, many=True)
        logger.error("Mostrando todos los usuarios sin paginacion")
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UsuariosSerializer)
    def post(self, request):

        logger.info("Peticicion POST para crear un nuevo usuario")
        serializer = UsuariosSerializer(data=request.data)
        #Validar los datos
        if serializer.is_valid():
            serializer.save() #Creacion del usuario
            logger.info("Usuario creado exitosamente")
            return Response({"message": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
        #En caso de error, retornar las validaciones
        logger.error("No se pudo crear el usuario: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuariosDetails(APIView):
    permission_classes = [IsAuthenticated, CustomPermission]
    model = Usuarios

    @swagger_auto_schema(responses={200: UsuariosSerializer()})
    def get(self, request, pk):
        """
        Obtener un usuario específico por su ID.
        """
        try:
            usuario = Usuarios.objects.get(pk=pk)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuariosSerializer(usuario)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UsuariosSerializer, responses={200: UsuariosSerializer()})
    def put(self, request, pk):
        """
        Actualizar completamente una unidad de medida por su ID.
        """
        logger.info("Solicitud PUT para actualizar el usuario con ID: %s", pk)
        try:
            usuarios = Usuarios.objects.get(pk=pk)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, usuarios) #Verificación de permisos
        serializer = UsuariosSerializer(usuarios, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Usuario actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar el usuario con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UsuariosSerializer, responses={200: UsuariosSerializer()})
    def patch(self, request, pk):
        """
        Actualizar parcialmente un usuario por su ID.
        """
        logger.info("Solicitud PATCH para actualizar parcialmente el usuario con ID: %s", pk)
        try:
            usuarios = Usuarios.objects.get(pk=pk)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, usuarios) #Verificación de permisos
        serializer = UsuariosSerializer(usuarios, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Usuario parcialmente actualizado exitosamente con ID: %s", pk)
            return Response(serializer.data)
        logger.error("No se pudo actualizar parcialmente el usuario con ID: %s. Errors: %s",
                     pk, serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        """
        Eliminar un usuario por su ID.
        """
        logger.info("Solicitud DELETE para eliminar un usuario con ID: %s", pk)
        try:
            usuarios = Usuarios.objects.get(pk=pk)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, usuarios) #Verificación de permisos
        usuarios.delete()
        logger.info("Usuario eliminado exitosamente con ID: %s", pk)
        return Response(status=status.HTTP_204_NO_CONTENT)