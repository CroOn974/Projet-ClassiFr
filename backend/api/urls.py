from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ModelViewset, AdminModelViewset, UserCreateAPIView, MonitorViewset,PredictImage, LabelViewset, UserDetailView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

model = DefaultRouter()
model.register('model', ModelViewset, basename= 'Model')

admin_model = DefaultRouter()
admin_model.register('admin/model', AdminModelViewset, basename= 'ad_Model')

monitor = DefaultRouter()
monitor.register('monitor',MonitorViewset, basename= 'monitor')

label = DefaultRouter()
label.register('label',LabelViewset, basename='label')

user = DefaultRouter()
user.register('user',UserDetailView, basename= "user")


urlpatterns = [
    path('signup/', UserCreateAPIView.as_view(), name='user_create'),
    path('api-token/', CustomTokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    path('', include(user.urls)),
    path('', include(model.urls)),
    path('', include(monitor.urls)),
    path('', include(admin_model.urls)),
    path('', include(label.urls)),
    path('predict', PredictImage, name="predict"),
]