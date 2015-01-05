# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_webpage_exists'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='webpage',
            options={'ordering': ['local_url']},
        ),
        migrations.RenameField(
            model_name='webpage',
            old_name='url',
            new_name='local_url',
        ),
        migrations.RemoveField(
            model_name='webpage',
            name='last_human_request',
        ),
        migrations.AlterField(
            model_name='webpage',
            name='content',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='webpage',
            unique_together=set([('local_url', 'website')]),
        ),
    ]
