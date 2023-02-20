from rest_framework import serializers
from api.models import Model

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'