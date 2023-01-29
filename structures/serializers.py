from .models import Structures
from rest_framework import serializers

class StructureSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        return Structures.objects.create(**validated_data)
    
    class Meta:
        model = Structures
        fields = ('name', 'city', 'address', 'rooms', 'image', 'owner', 'id', 'description', 'restaurants', 'pool', 'spa')