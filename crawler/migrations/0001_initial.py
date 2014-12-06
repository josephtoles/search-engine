# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Webpage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('robots_allowed', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_human_request', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'ordering': ['url'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('exists', models.BooleanField(default=False)),
                ('robots_exists', models.BooleanField(default=False)),
                ('robots_content', models.TextField()),
                ('robots_updated', models.DateTimeField()),
            ],
            options={
                'ordering': ['url'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='webpage',
            name='website',
            field=models.ForeignKey(to='crawler.Website'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='webpage',
            unique_together=set([('url', 'website')]),
        ),
    ]
