from django.conf import settings
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='events',
    )

    def __str__(self):
        return self.name
