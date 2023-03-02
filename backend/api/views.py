import json
from api.models import Model, DateCreate, Associer, Predict
from api.serializers import ModelSerializer, PredictSerializer
from rest_framework.permissions import IsAuthenticated
#API
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
#Pred
from PIL import Image
from tensorflow import keras
import matplotlib as plt
import numpy as np

#View destiné au admin
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

    # fonction qui permet la création personalisé d'un modèle
    def create(self, request, *args, **kwargs):

        date = getToday()
        
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


class MonitorViewset(viewsets.ModelViewSet):
    queryset = Predict.objects.all()
    serializer_class = PredictSerializer

    # fonction qui permet enregistrer
    def create(self, request, *args, **kwargs):

        date = getToday()
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        my_predict = Predict.objects.create(
            image=serializer.validated_data['name'],
            bonne_pred=serializer.validated_data['mod_file'],
            libele=serializer.validated_data['accuracy'],
            jour= date,
            id_model=serializer.validated_data['status'],
            feedback=serializer.validated_data['info']
        )

        serializer = self.get_serializer(my_predict)
        return Response(serializer.data)

# http://localhost:8000/api/predict -> Methode POST, reçois des images et retourn la prédiction
@api_view(['POST'])
def Predict(request):
    images = request.FILES.getlist('images')
    model = request.POST.get('selectedOption')
    results = doPred(images,model)
    response_data = json.dumps(results)
    print(response_data)
    return Response(data=response_data, content_type='application/json')
    
    
def doPred(images,model):
    results = []
    modelFile = getModelFiles(model)
    cathegories = getCategories(model)
    modelPredict = keras.models.load_model("api/modelPred/"+modelFile+".keras")
    
    for image in images:
        img_norm = norm_img(image)
        predictions = modelPredict.predict(img_norm)
        print(predictions)
        pred_w_label = addLabelToPredic(predictions, cathegories)
        result = {
            'image': str(image),
            'prediction': pred_w_label
        }
        print(result)
        results.append(result)

    return results

# normalise les images
def norm_img(img_file):
    img = Image.open(img_file)
    img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# récupère la date
def getToday():
    from datetime import date
    today = date.today()

    # verifie si la date existe déjà dans la bdd
    if DateCreate.objects.filter(jour = today):
        # si elle existe la récupère
        date = DateCreate.objects.get(jour = today)
    else:
        # si elle existe pas la crée
        date = DateCreate.objects.create(jour = today)

    return date

# obtenir les catégories à partir de l'emplacement de répertoire
def getCategories(id):
    try:
        labels = Associer.objects.filter(id_model=id).values_list('libele__libele', flat=True).order_by('libele__libele')
        return labels
    except Model.DoesNotExist:
        return None

# retourne l'emplacement du fichier
def getModelFiles(id_model):
    try:
        model = Model.objects.get(id_model=id_model)
        return model.mod_file
    except Model.DoesNotExist:
        return None

# récupère l'object model  
def getModel(id_model):
    try:
        model = Model.objects.get(id_model=id_model)
        return model
    except Model.DoesNotExist:
        return None

# Associer les prédiction au label
def addLabelToPredic(predictions, categories):
    img_pred = []

    print(predictions)
    
    for i in range(len(categories)):
        img_pred.append((categories[i], predictions[0][i]))
    # Tri des prédictions par ordre décroissant de probabilité
    img_pred.sort(key=lambda x: x[1], reverse=True)
    # Récupération de la catégorie avec la plus haute probabilité
    prediction = {
        'label':img_pred[0][0],
        'pourcentage':img_pred[0][1]*100
    }
    return prediction