from django.urls import path

from apps.events.views import create_event, list_event_participants, signup_for_event

urlpatterns = [
    path("events/", create_event, name="event-create"),
    path(
        "events/<int:event_id>/participants/",
        list_event_participants,
        name="event-participants-list",
    ),
    path(
        "events/<int:event_id>/signup/",
        signup_for_event,
        name="event-signup",
    ),
]
