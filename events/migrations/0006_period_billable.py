# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150623_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='billable',
            field=models.BooleanField(default=True),
        ),
    ]
