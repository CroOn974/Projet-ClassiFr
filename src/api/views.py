from api.models import Model
from api.serializers import ItemSerializer
from rest_framework import viewsets


class ModelViewset(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ItemSerializer


