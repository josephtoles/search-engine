# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0005_auto_20150104_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpage',
            name='exists',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='webpage',
            name='robots_allowed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
