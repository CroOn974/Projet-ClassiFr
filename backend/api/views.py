import json
from django.shortcuts import get_object_or_404
from api.models import Model, DateCreate, Associer, Predict, Label
from api.serializers import ModelSerializer, PredictSerializer, LabelSerializer
from rest_framework.permissions import IsAuthenticated
#API
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
#User Login
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
#Pred
from PIL import Image
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.layers import Dense
from keras.layers import BatchNormalization
from keras.models import Model as mod
import matplotlib as plt
import numpy as np
#os
import os
import uuid
import base64
import io


# View destiné au admin
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

    def create(self, request, *args, **kwargs):
            data = request.data.copy()
            data['jour'] = getToday()

            labels_list = data['labels']

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            instance = serializer.instance
            newModelId = instance.id_model

            associer_list = []
            for label_name in labels_list:
                # Récupérer ou créer une instance de Label en fonction du nom de libellé donné
                label, created = Label.objects.get_or_create(libele=label_name)
                associer = Associer(libele=label, id_model=instance)
                associer_list.append(associer)
            Associer.objects.bulk_create(associer_list)

            accuracy = createModel(labels_list,newModelId)

            mod_file = 'model_{}'.format(newModelId)
                # Mettre à jour le champ mod_file du modèle créé
            instance.mod_file = mod_file
            instance.accuracy = accuracy
            instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

    # permet de changé le status d'un modèle
    @action(detail=True, methods=['POST'])
    def etatStatus(self, request, pk):
        model = self.get_object()
        model.etatStatus()
        serializer = self.get_serializer(model)
        return Response(serializer.data)


    @action(detail=True, methods=['GET'])
    def updateInfo(self, request, pk=None):
        # récupérer le modèle spécifié par l'ID
        model = get_object_or_404(Predict, id=pk)
        # récupérer toutes les prédictions associées à ce modèle
        predictions = Predict.objects.filter(id_model=model)
        # sérialiser les prédictions
        serializer = PredictSerializer(predictions, many=True)
        # renvoyer les prédictions sérialisées en réponse
        return Response(serializer.data)
    

# View destiné au client
class ModelViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Model.objects.filter(status = True)
    serializer_class = ModelSerializer

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MonitorViewset(viewsets.ModelViewSet):
    queryset = Predict.objects.all()
    serializer_class = PredictSerializer

    # fonction qui permet enregistrer
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = getToday()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        my_predict = Predict.objects.create(
            image=serializer.validated_data['image_file'],
            bonne_pred=serializer.validated_data['bonne_pred'],
            libele=serializer.validated_data['libele'],
            jour= date,
            id_model=serializer.validated_data['id_model'],
            feedback=serializer.validated_data['feedback']
        )

        serializer = self.get_serializer(my_predict)
        return Response(serializer.data)
    
        # permet de changé le status d'un modèle
    
    @action(detail=True, methods=['POST'])
    def moniModel(self, request, pk):
        monitor = self.get_object()
        model.etatStatus()
        serializer = self.get_serializer(model)
        return Response(serializer.dat)
    
class LabelViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


# http://localhost:8000/api/predict -> Methode POST, reçois des images et retourn la prédiction
@api_view(['POST'])
def PredictImage(request):
    # récupère les image et le modèle
    images = request.FILES.getlist('images')
    model = request.POST.get('selectedOption')

    results = doPred(images,model)
    response_data = json.dumps(results)

    return Response(data=response_data, content_type='application/json')
    
    
def doPred(images,model):
    results = []
    modelFile = getModelFiles(model)
    cathegories = getCategories(model)
    modelPredict = keras.models.load_model("api/modelPred/"+modelFile+".keras")
    
    for image in images:
        img_norm = norm_img(image)
        predictions = modelPredict.predict(img_norm)
        pred_w_label = addLabelToPredic(predictions, cathegories)
        result = {
            'image': str(image),
            'prediction': pred_w_label
        }
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

    return today

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

# récupère l'object model selon l'id
def getModel(id_model):
    try:
        model = Model.objects.get(id_model=id_model)
        return model
    except Model.DoesNotExist:
        return None

# Associer les prédiction au label
def addLabelToPredic(predictions, categories):
    img_pred = []

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

# création du modèles de prediction
def createModel(labels_list, newModelId):

    nbLabel = len(labels_list)

    # Define the number of epochs and batch size
    epochs = 5
    batch_size = 128
    image_size = (224,244)

    # Use ImageDataGenerator for data augmentation
    datagen = ImageDataGenerator(
        rescale=1./255.0,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
    

    folder = labels_list

    train_ds = datagen.flow_from_directory(
    "api/dataset/train_set",
    target_size=image_size,
    batch_size=batch_size,
    classes=folder,
    class_mode='categorical')

    val_ds = datagen.flow_from_directory(
    "api/dataset/test_set/",
    target_size=image_size,
    batch_size=batch_size,
    classes=folder,
    class_mode='categorical')

    # Charger le modèle pré-entraîné
    # include_top=False , choix de vouloir ou non les couches de décisions
    baseModel = MobileNetV2(input_shape=(224, 224,3), 
                            alpha=1.0, 
                            include_top=False, 
                            weights='imagenet', 
                            input_tensor=None, 
                            pooling='max')

    # Gèle les couches basses du réseau
    for layer in baseModel.layers:
        layer.trainable=False

    # Ajoutez une couche de normalisation BatchNormalization après la première couche dense
    topModel = Dense(4096, activation='relu', trainable=True)(baseModel.output)
    topModel = BatchNormalization()(topModel)
    topModel = Dense(nbLabel, activation='sigmoid', trainable=True)(topModel)

    newmod = mod(inputs=baseModel.input, outputs=topModel)
    # Compiler le modèle pour la formation
    newmod.compile(optimizer='adam', loss='categorical_hinge', metrics=['accuracy'])

    try:
    # bloc de code susceptible de lever une exception
        newModel = newmod.fit(
                    train_ds,
                    epochs=epochs,
                    validation_data=val_ds,
        )

   
    except:
        print("erreur entrainement du model")

    # Sauvegarde du modèle
    mod_file = f"api/modelPred/model_{newModelId}.keras"
    newmod.save(mod_file, save_format="h5")

    accuracy = newModel.history['accuracy'][epochs - 1]

    return accuracy


