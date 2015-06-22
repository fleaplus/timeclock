from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import TimeclockUser


class Event(models.Model):
    time = models.DateTimeField()
    user = models.ForeignKey(TimeclockUser)

    def __str__(self):
        return str(self.time)

    def save(self, *args, **kwargs):
        last_event = Event.objects.filter(user=self.user).last()
        super().save(*args, **kwargs)
        if last_event and not last_event.start.count() and not last_event.end.count():
            Period(user=self.user, start=last_event, end=self).save()


class Period(models.Model):
    user = models.ForeignKey(TimeclockUser)
    start = models.ForeignKey(Event, related_name='start')
    end = models.ForeignKey(Event, related_name='end')

    def save(self, *args, **kwargs):
        if self.start.user == self.user and self.end.user == self.user:
            return super().save(*args, **kwargs)
        else:
            raise ValidationError('Event user must match period user.')

    @property
    def duration(self):
        return (self.end.time - self.start.time)
