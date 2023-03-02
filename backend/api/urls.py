from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ModelViewset, AdminModelViewset, MonitorViewset,Predict

model = DefaultRouter()
model.register('model', ModelViewset, basename= 'Model')

admin_model = DefaultRouter()
admin_model.register('admin/model', AdminModelViewset, basename= 'Model')

monitor = DefaultRouter()
monitor.register('monitor',MonitorViewset, basename= "monitor")

urlpatterns = [
    path('', include(model.urls)),
    path('', include(monitor.urls)),
    path('', include(admin_model.urls)),
    path('predict', Predict, name="predict"),
]