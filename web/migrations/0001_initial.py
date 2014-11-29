# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
            name='WebpageRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
                ('search', models.ForeignKey(to='web.Search')),
                ('webpage', models.ForeignKey(to='web.Webpage')),
            ],
            options={
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
            field=models.ForeignKey(to='web.Website'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='webpage',
            unique_together=set([('url', 'website')]),
        ),
        migrations.AddField(
            model_name='search',
            name='webpages',
            field=models.ManyToManyField(to='web.Webpage', through='web.WebpageRating'),
            preserve_default=True,
        ),
    ]
