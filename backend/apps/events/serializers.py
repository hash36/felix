from rest_framework import serializers

from apps.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'participants']


class EventSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name']
