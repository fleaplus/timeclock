from django.db import models
from django.utils import timezone

from accounts.models import TimeclockUser


class Event(models.Model):
    time = models.DateTimeField()
    user = models.ForeignKey(TimeclockUser)

    def __str__(self):
        return str(self.time)

    def save_without_period_update(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        billable = kwargs.pop('billable', True)
        super().save(*args, **kwargs)
        Period.objects.event_occurred(self, billable=billable)


class PeriodManager(models.Manager):
    def event_occurred(self, event, billable=True):
        """
        Update the user's incomplete period
        """
        period, created = Period.objects.get_or_create(user=event.user, completed=False)

        if created:
            period.start = event
        else:
            period.end = event
            period.completed = True
        period.billable = billable
        period.save()


class Period(models.Model):
    user = models.ForeignKey(TimeclockUser)
    start = models.ForeignKey(Event, related_name='start', null=True)
    end = models.ForeignKey(Event, related_name='end', null=True)
    completed = models.BooleanField(default=True)
    billable = models.BooleanField(default=True)

    objects = PeriodManager()

    @property
    def duration(self):
        if self.end:
            return (self.end.time - self.start.time)
        else:
            return (timezone.now() - self.start.time)
