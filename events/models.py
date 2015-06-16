from django.db import models


class Event(models.Model):
    time = models.DateTimeField()
