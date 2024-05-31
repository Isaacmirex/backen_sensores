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
                # Obtener el último usuario ingresado, si existe
                try:
                    ultimo_usuario = Usuario.objects.latest('usr_id')
                except Usuario.DoesNotExist:
                    ultimo_usuario = None
                
                # Obtener la última encuesta del usuario, si el usuario existe
                if ultimo_usuario:
                    try:
                        ultima_encuesta = Encuesta.objects.filter(usr=ultimo_usuario).latest('ec_id')
                    except Encuesta.DoesNotExist:
                        ultima_encuesta = None
                else:
                    ultima_encuesta = None
                
                # Obtener los sensores recién creados
                try:
                    sensores = Sensores.objects.get(pk=response.data['sen_id'])
                except Sensores.DoesNotExist:
                    return Response({"error": "No se encontraron datos de sensores recién creados."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Calcular el estrés solo si tenemos usuario y encuesta
                if ultimo_usuario and ultima_encuesta:
                    estres = calcular_estres(ultimo_usuario, ultima_encuesta, sensores)
                    # Actualizar el campo usr_estres del último usuario
                    ultimo_usuario.usr_estres = estres
                    ultimo_usuario.save()
                    print(f"Estres calculado: {estres}")  # Debug print para confirmar el cálculo
                else:
                    # Manejar el caso donde no hay usuario o encuesta
                    return Response({"warning": "No se pudo calcular el estrés por falta de usuario o encuesta."}, status=status.HTTP_200_OK)
            
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return response

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
