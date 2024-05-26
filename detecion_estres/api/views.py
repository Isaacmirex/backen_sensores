from rest_framework import viewsets, status
from rest_framework.response import Response
from detecion_estres.models import Encuesta, Sensores, Usuario
from detecion_estres.api.serializer import EncuestaSerializer, SensoresSerializer, UsuarioSerializer
from detecion_estres.estres import calcular_estres

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
                # Obtener el último usuario ingresado
                ultimo_usuario = Usuario.objects.latest('usr_id')
                # Obtener la última encuesta del usuario
                ultima_encuesta = Encuesta.objects.filter(usr=ultimo_usuario).latest('ec_id')
                # Obtener los sensores recién creados
                sensores = Sensores.objects.get(pk=response.data['sen_id'])
                
                # Calcular el estrés
                estres = calcular_estres(ultimo_usuario, ultima_encuesta, sensores)
                
                # Actualizar el campo usr_estres del último usuario
                ultimo_usuario.usr_estres = estres
                ultimo_usuario.save()
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return response

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
