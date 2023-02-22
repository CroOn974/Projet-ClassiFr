from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import DateViewset, ModelViewset, AdminModelViewset 

model = DefaultRouter()
model.register('model', ModelViewset, basename= 'Model')

admin_model = DefaultRouter()
admin_model.register('admin/model', AdminModelViewset, basename= 'Model')

date = DefaultRouter()
date.register('date',DateViewset, basename= "date")

urlpatterns = [
    path('', include(model.urls)),
    path('', include(date.urls)),
    path('', include(admin_model.urls)),
]