from rest_framework import viewsets
from detecion_estres.models import Encuesta, Sensores, Usuario
from detecion_estres.api.serializer import EncuestaSerializer, SensoresSerializer, UsuarioSerializer

class EncuestaViewSet(viewsets.ModelViewSet):
    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer

class SensoresViewSet(viewsets.ModelViewSet):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
