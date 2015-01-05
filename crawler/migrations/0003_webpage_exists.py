# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_auto_20141206_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpage',
            name='exists',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
    ]
