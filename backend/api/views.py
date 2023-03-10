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
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
#User Login
from rest_framework.generics import CreateAPIView, RetrieveAPIView
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

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

##
# View Model pour admin
# EndPoint -> http://localhost:8000/api/admin/model/
#
class AdminModelViewset(viewsets.ModelViewSet):
    
    serializer_class = ModelSerializer
    ##
    # Retourne la liste des modèle dont le status est "True"
    # EndPoint -> http://localhost:8000/api/admin/model
    # Method -> POST
    # Return -> QuerySet
    #
    def get_queryset(self):
        
        # retourne tous les modèles
        queryset = Model.objects.all()

        # retourne les modèle selon le status
        status = self.request.GET.get('status')
        if status is not None:
            queryset = Model.objects.filter(status = status)
        return queryset

    ##
    # Creation de modèle
    # Attend un dictionnaire contenant
        # name = CharField(max_length=50)
        # mod_file = CharField(max_length=255)
        # accuracy = DecimalField(decimal_places=4, max_digits=15)
        # jour = PrimaryKeyRelatedField(allow_null=True, queryset=DateCreate.objects.all(), required=False)
        # status = BooleanField(allow_null=True, required=False)
        # info = CharField(allow_blank=True, allow_null=True, max_length=255, required=False)
        # labels = SerializerMethodField()
    #
    # EndPoint -> http://localhost:8000/api/admin/model/
    # Method -> POST
    #
    def create(self, request, *args, **kwargs):
            
            data = request.data.copy()
            data['jour'] = getToday()

            # récupère les labèles contenue dans la requete
            labels_list = data['labels']

            # récupère les données contenue dans le request
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            # recupère l'instance pour pouvoir la modifier
            instance = serializer.instance
            newModelId = instance.id_model

            # associe le modèle avec les labèle
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
        

    ##
    # permet de modifier le status du modèle
    # Parameter -> id du modèle
    # EndPoint -> http://localhost:8000/api/admin/model/'+ id +'/etatStatus/
    # Method -> POST
    #
    #
    @action(detail=True, methods=['POST'])
    def etatStatus(self, request, pk):
        model = self.get_object()
        model.etatStatus()
        serializer = self.get_serializer(model)
        return Response(serializer.data)

    ##
    # permet de modifier le champs info du modèle
    # Parameter -> id du modèle
    # EndPoint -> http://localhost:8000/api/admin/model/'+ id +'/updateInfo/
    # Method -> POST
    #
    #
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
    
##
# View Model pour user
# EndPoint -> http://localhost:8000/api/model/
#
class ModelViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Model.objects.filter(status = True)
    serializer_class = ModelSerializer

##
# Recupère les information sur les users
# EndPoint -> http://localhost:8000/api/user/
#
class UserDetailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

##
# Permet de crée un user
# Parameter
# # username 
# # password
# #
# EndPoint -> http://localhost:8000/api/signup/
#
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

##
# View Model pour user
# EndPoint -> http://localhost:8000/api/monitor/
#
class MonitorViewset(viewsets.ModelViewSet):
    queryset = Predict.objects.all()
    serializer_class = PredictSerializer

    ##
    # Retour utilisateur sur une image
    # Attend un dictionnaire contenant
        # image_file 
        # bonne_pred 
        # libele
        # jour
        # id_model
        # feedback
    #
    # EndPoint -> http://localhost:8000/api/monitor/
    # Method -> POST
    #
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = getJour()
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
    

    ##
    # Enregistre le feedback sur une prédiction
    # EndPoint -> http://localhost:8000/api/monitor/id -> id de la prédiction
    # Method -> PATCH
    # 
    #
    @action(detail=True, methods=['patch'])
    def update_feedback(self, request, pk=None):
        predict = self.get_object()
        predict.feedback = request.data.get('feedback', predict.feedback)
        predict.save()
        serializer = self.get_serializer(predict)
        
    ##
    # Récupère les prédiction selon le modèle
    # EndPoint -> http://localhost:8000/api/monitor/id/moniModel -> id de la prédiction
    # Method -> GET
    # 
    #
    @action(detail=True, methods=['GET'])
    def moniModel(self, request, pk):
        id_model = self.kwargs.get('pk')
        if int(id_model) > 0:
            queryset = Predict.objects.filter(id_model=id_model).order_by('id_predict')
        else:
            queryset = Predict.objects.all().order_by('id_predict')

        print(queryset)
        serializer = PredictSerializer(queryset, many=True)
        return Response(serializer.data)

##
# Récupère la liste des labèles
# EndPoint -> http://localhost:8000/api/label/
#   
class LabelViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    
##
# Réalisé des prédictions sur les image envoyer
# Parameter
# # Liste d'image
# # Modèle
# EndPoint -> http://localhost:8000/api/predict
# Methood -> POST
#
@api_view(['POST'])
def PredictImage(request):
    # récupère les image et le modèle
    images = request.FILES.getlist('images')
    model = request.POST.get('selectedOption')

    results = doPred(images,model)
    response_data = json.dumps(results)

    return Response(data=response_data, content_type='application/json')
    
##
# Fonction qui retourne la prédiction
# Parameter
# # liste d'image
# # modèle
# Return liste contenant 
# # {   
# #    image:,
# #    prediction:
# # }
# #
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

##
# Fonction qui normalise les image
# Parameter
# # 1 image
# Return
# # 1 image
#
def norm_img(img_file):
    img = Image.open(img_file)
    img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

##
# Récupère la date du jour
# return string
#
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

##
# Récupère la date du jour
# return Object
#
def getJour():
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

##
# Récupère la liste des labèle selon le modèle
# Parameter 
# # id du modèle
# return
# # liste contenant les labèles
#
def getCategories(id):
    try:
        labels = Associer.objects.filter(id_model=id).values_list('libele__libele', flat=True).order_by('libele__libele')
        return labels
    except Model.DoesNotExist:
        return None

##
# Récupère l'emplacement du fichier
# Parameter 
# # id du modèle
# return
# # String
#
def getModelFiles(id_model):
    try:
        model = Model.objects.get(id_model=id_model)
        return model.mod_file
    except Model.DoesNotExist:
        return None

##
# Récupère le modèle
# Parameter 
# # id du modèle
# return
# # Object
#
def getModel(id_model):
    try:
        model = Model.objects.get(id_model=id_model)
        return model
    except Model.DoesNotExist:
        return None

##
# Associe les prediciton a leur labèles
# Parameter 
# # liste de prédiction
# # liste de catégorie
# return
# # Object
# # {
# #     'label':    ,
# #     'pourcentage: 
# # }
#
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

##
# Fonction qui permet de crée des modèle de prédiction
# Parameter  
# # liste des labèles
# # id du modèle crée
# Return
# # Integer
#
#
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


