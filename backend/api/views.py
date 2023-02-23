from api.models import Model, DateCreate
from api.serializers import ModelSerializer, DateSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date

#View destiné au admin
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

    # fonction qui permet la création personalisé d'un modèle
    def create(self, request, *args, **kwargs):
        from datetime import date
        today = date.today()
        
        # verifie si la date existe déjà dans la bdd
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


# View destiné au client
class ModelViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Model.objects.filter(status = True)
    serializer_class = ModelSerializer

 
class DateViewset(viewsets.ModelViewSet):
    queryset = DateCreate.objects.all()
    serializer_class = DateSerializer