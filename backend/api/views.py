from api.models import Model, DateCreate
from api.serializers import ModelSerializer, DateSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date


class AdminModelViewset(viewsets.ModelViewSet):
    
    serializer_class = ModelSerializer

    def get_queryset(self):
        # retourne tous les modèles
        queryset = Model.objects.all()

        # retourne les modèle selon le status
        status = self.request.GET.get('status')
        if status is not None:
            queryset = Model.objects.filter(status = status)
        return queryset

    def perform_create(self, serializer):
        today = date.today()
        if DateCreate.objects.filter(jour = today):
            date = DateCreate.objects.get(jour = today)
        else:
            date = DateCreate.objects.create(jour = today)

        serializer.save(jour = date)
        

    # permet de changé le status d'un modèle
    @action(detail=True, methods=['POST'])
    def etatStatus(self, request, pk):
        model = self.get_object()
        model.etatStatus()
        serializer = self.get_serializer(model)
        return Response(serializer.data)


class ModelViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Model.objects.filter(status = True)
    serializer_class = ModelSerializer

 
class DateViewset(viewsets.ModelViewSet):
    queryset = DateCreate.objects.all()
    serializer_class = DateSerializer