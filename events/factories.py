import factory

from django.utils import timezone

from . import models

from accounts.factories import EmployeeFactory


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    time = timezone.now()
    user = factory.SubFactory(EmployeeFactory)
