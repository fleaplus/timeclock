# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='completed',
            field=models.BooleanField(default=True),
        ),
    ]
