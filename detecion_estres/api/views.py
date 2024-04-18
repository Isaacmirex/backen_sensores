from rest_framework import viewsets
from rest_framework.response import Response
from detecion_estres.models import Encuesta,Sensores,Usuario
from detecion_estres.api.serializer import EncuestaSerializer , SensoresSerializer,UsuarioSerializer

class EncuestaViewSet(viewsets.ViewSet):
    def list(self, request):
        encuestas = Encuesta.objects.all()
        serializer = EncuestaSerializer(encuestas, many=True)
        return Response(serializer.data)

class SensoresViewSet(viewsets.ViewSet):
    def list(self, request):
        sensores = Sensores.objects.all()
        serializer = SensoresSerializer(sensores, many=True)
        return Response(serializer.data)

class UsuarioViewSet(viewsets.ViewSet):
    def list(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)