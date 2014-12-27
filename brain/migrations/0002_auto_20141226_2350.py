# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('brain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='title',
            field=models.CharField(default=b'', max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
