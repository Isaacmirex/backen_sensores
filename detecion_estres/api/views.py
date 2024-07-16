from rest_framework import viewsets, status
from rest_framework.response import Response
from detecion_estres.models import Encuesta, Sensores, Usuario
from detecion_estres.api.serializer import EncuestaSerializer, SensoresSerializer, UsuarioSerializer
from detecion_estres.estres import calcular_estres
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EncuestaViewSet(viewsets.ModelViewSet):
    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer

class SensoresViewSet(viewsets.ModelViewSet):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            try:
                # Obtener el último usuario ingresado, si existe
                try:
                    ultimo_usuario = Usuario.objects.latest('usr_id')
                    logger.debug(f"Último usuario obtenido: {ultimo_usuario.usr_id}")
                except Usuario.DoesNotExist:
                    ultimo_usuario = None
                    logger.warning("No se encontró ningún usuario.")
                
                # Obtener la última encuesta del usuario, si el usuario existe
                if ultimo_usuario:
                    try:
                        ultima_encuesta = Encuesta.objects.filter(usr=ultimo_usuario).latest('ec_id')
                        logger.debug(f"Última encuesta obtenida para el usuario {ultimo_usuario.usr_id}: {ultima_encuesta.ec_id}")
                    except Encuesta.DoesNotExist:
                        ultima_encuesta = None
                        logger.warning(f"No se encontró ninguna encuesta para el usuario {ultimo_usuario.usr_id}.")
                else:
                    ultima_encuesta = None
                
                # Obtener los sensores recién creados
                try:
                    sensores = Sensores.objects.get(pk=response.data['sen_id'])
                    logger.debug(f"Sensores recién creados obtenidos: {sensores.sen_id}")
                except Sensores.DoesNotExist:
                    logger.error("No se encontraron datos de sensores recién creados.")
                    return Response({"error": "No se encontraron datos de sensores recién creados."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Calcular el estrés solo si tenemos usuario y encuesta
                if ultimo_usuario and ultima_encuesta:
                    estres = calcular_estres(ultimo_usuario, ultima_encuesta, sensores)
                    # Actualizar el campo usr_estres del último usuario
                    ultimo_usuario.usr_estres = estres
                    ultimo_usuario.save()
                    logger.debug(f"Estrés calculado: {estres} para el usuario {ultimo_usuario.usr_id}")
                else:
                    logger.warning("No se pudo calcular el estrés por falta de usuario o encuesta.")
                    return Response({"warning": "No se pudo calcular el estrés por falta de usuario o encuesta."}, status=status.HTTP_200_OK)
            
            except ValueError as e:
                logger.error(f"Error de valor: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return response

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
