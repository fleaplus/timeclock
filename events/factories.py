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

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.save_without_period_update()
        return obj


class PeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Period

    user = factory.SubFactory(EmployeeFactory)
    start = factory.SubFactory(EventFactory, user=factory.SelfAttribute('..user'), time=(timezone.now()-timedelta(hours=1)))
    end = factory.SubFactory(EventFactory, user=factory.SelfAttribute('..user'))
