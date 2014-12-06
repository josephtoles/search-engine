# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='robots_updated',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
