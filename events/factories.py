import factory

from django.utils import timezone
from datetime import timedelta

from . import models

from accounts.factories import EmployeeFactory


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    time = timezone.now()
    user = factory.SubFactory(EmployeeFactory)


class PeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Period

    user = factory.SubFactory(EmployeeFactory)
    start = factory.SubFactory(EventFactory, user=factory.SelfAttribute('..user'), time=(timezone.now()-timedelta(hours=1)))
    end = factory.SubFactory(EventFactory, user=factory.SelfAttribute('..user'))
