from .models import Reservations
from rest_framework import serializers


class ReservationseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ('user', 'structure', 'room', 'date_from', 'date_to')

    def create(self, validated_data):
        return Reservations.objects.create(**validated_data)
