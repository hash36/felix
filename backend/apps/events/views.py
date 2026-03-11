from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Event
from apps.events.serializers import EventSerializer, EventSignupSerializer
from apps.users.serializers import UserSerializer


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_event_participants(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return Response(UserSerializer(event.participants.all(), many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def signup_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.participants.add(request.user)
    return Response(EventSignupSerializer(event).data)
