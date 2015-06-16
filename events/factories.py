import factory

from django.utils import timezone

from . import models


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    time = timezone.now()