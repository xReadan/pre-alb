from .models import StructureRooms
from rest_framework import serializers

class StructureRoomsSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        return StructureRooms.objects.create(**validated_data)
    
    class Meta:
        model = StructureRooms
        fields = '__all__'