from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.events.models import Event

User = get_user_model()


class EventCreationTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            is_staff=True,
        )
        self.regular = User.objects.create_user(
            username="regular",
            email="regular@example.com",
            password="regularpass",
        )

    def _get_token(self, user):
        response = self.client.post(
            "/auth/token/",
            {
                "username": user.username,
                "password": "adminpass" if user.is_staff else "regularpass",
            },
            format="json",
        )
        return response.json()["token"]

    def test_admin_can_create_event(self):
        token = self._get_token(self.admin)
        response = self.client.post(
            "/events/",
            {"name": "Launch Party"},
            format="json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], "Launch Party")
        self.assertEqual(Event.objects.count(), 1)

    def test_regular_user_cannot_create_event(self):
        token = self._get_token(self.regular)
        response = self.client.post(
            "/events/",
            {"name": "Sneaky Event"},
            format="json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_create_event(self):
        response = self.client.post("/events/", {"name": "Ghost Event"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_name_is_required(self):
        token = self._get_token(self.admin)
        response = self.client.post(
            "/events/",
            {"name": ""},
            format="json",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EventParticipantTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass",
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="alicepass",
        )
        self.event = Event.objects.create(name="Test Event")

    def _get_token(self, user, password):
        response = self.client.post(
            "/auth/token/",
            {"username": user.username, "password": password},
            format="json",
        )
        return response.json()["token"]

    def test_authenticated_user_can_join_event(self):
        token = self._get_token(self.user, "alicepass")
        response = self.client.post(
            f"/events/{self.event.id}/signup/",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.event.id)
        self.assertEqual(response.json()["name"], self.event.name)
        self.assertNotIn("participants", response.json())
        self.assertTrue(self.event.participants.filter(id=self.user.id).exists())

    def test_unauthenticated_cannot_join_event(self):
        response = self.client.post(f"/events/{self.event.id}/signup/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_joining_nonexistent_event_returns_404(self):
        token = self._get_token(self.user, "alicepass")
        response = self.client.post(
            "/events/99999/signup/",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_joining_same_event_twice_is_idempotent(self):
        token = self._get_token(self.user, "alicepass")
        self.client.post(
            f"/events/{self.event.id}/signup/",
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        response = self.client.post(
            f"/events/{self.event.id}/signup/",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("participants", response.json())
        self.assertEqual(self.event.participants.filter(id=self.user.id).count(), 1)

    def test_admin_can_list_participants(self):
        self.event.participants.add(self.user)
        token = self._get_token(self.admin, "adminpass")
        response = self.client.get(
            f"/events/{self.event.id}/participants/",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [u["id"] for u in response.json()]
        self.assertIn(self.user.id, ids)

    def test_regular_user_cannot_list_participants(self):
        token = self._get_token(self.user, "alicepass")
        response = self.client.get(
            f"/events/{self.event.id}/participants/",
            HTTP_AUTHORIZATION=f"Token {token}",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_participants(self):
        response = self.client.get(f"/events/{self.event.id}/participants/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
