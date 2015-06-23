# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_period_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='end',
            field=models.ForeignKey(null=True, related_name='end', to='events.Event'),
        ),
        migrations.AlterField(
            model_name='period',
            name='start',
            field=models.ForeignKey(null=True, related_name='start', to='events.Event'),
        ),
    ]
