from  rest_framework.routers import  DefaultRouter
from  detecion_estres.api.views import  EncuestaViewSet,SensoresViewSet,UsuarioViewSet

router = DefaultRouter()
router.register(r'encuestas', EncuestaViewSet, basename='encuesta')
router.register(r'sensores', SensoresViewSet, basename='sensores')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
urlpatterns = router.urls
