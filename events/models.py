from django.db import models

from accounts.models import TimeclockUser


class Event(models.Model):
    time = models.DateTimeField()
    user = models.ForeignKey(TimeclockUser)
