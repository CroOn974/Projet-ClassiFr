from rest_framework import serializers
from api.models import Model, DateCreate

class ModelSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()

    class Meta:
        model = Model
        fields = ('id_model','name', 'mod_file', 'accuracy', 'jour', 'status', 'info', 'labels')

    def get_labels(self, obj):
        return [associer.libele.libele for associer in obj.associer_set.all()]

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateCreate
        fields = '__all__'

        