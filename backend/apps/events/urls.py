from django.urls import path

from apps.events.views import create_event, event_participants

urlpatterns = [
    path("events/", create_event, name="event-create"),
    path(
        "events/<int:event_id>/participants/",
        event_participants,
        name="event-participants",
    ),
]
