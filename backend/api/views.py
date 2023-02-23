from api.models import Model, DateCreate
from api.serializers import ModelSerializer, DateSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date


class AdminModelViewset(viewsets.ModelViewSet):
    
    serializer_class = ModelSerializer

    def get_queryset(self):
        print('ttttt')
        # retourne tous les modèles
        queryset = Model.objects.all()

        # retourne les modèle selon le status
        status = self.request.GET.get('status')
        if status is not None:
            queryset = Model.objects.filter(status = status)
        return queryset

    # def perform_create(self, serializer):
    #     print('ttttt')

    #     print(serializer.validated_data)
    #     today = date.today()
        
    #     if DateCreate.objects.filter(jour = today):
    #         date = DateCreate.objects.get(jour = today)
    #     else:
    #         date = DateCreate.objects.create(jour = today)

    #     name = serializer.validated_name.get('name')
    #     mod_file = name 

    #     serializer.save(jour = date, mod_file = mod_file)

    def create(self, request, *args, **kwargs):
        from datetime import date
        print('rrrrr')
        print(request)
        today = date.today()
        
        if DateCreate.objects.filter(jour = today):
            date = DateCreate.objects.get(jour = today)
        else:
            date = DateCreate.objects.create(jour = today)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # création de l'objet MyModel
        my_model = Model.objects.create(
            name=serializer.validated_data['name'],
            mod_file=serializer.validated_data['mod_file'],
            accuracy=serializer.validated_data['accuracy'],
            jour= date,
            status=serializer.validated_data['status'],
            info=serializer.validated_data['info']
        )
        # sérialisation et retour de la réponse
        serializer = self.get_serializer(my_model)
        return Response(serializer.data)
        

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