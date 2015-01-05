# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0004_auto_20150104_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpage',
            name='exists',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
