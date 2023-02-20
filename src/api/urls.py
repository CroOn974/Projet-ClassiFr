from rest_framework.routers import DefaultRouter
from api.views import ModelViewset

router = DefaultRouter()

router.register('model', ModelViewset, basename='test')

urlpatterns = router.urls
