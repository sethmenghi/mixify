# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0003_auto_20151020_1958'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mixtape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name of Mixtape', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('provider_id', models.CharField(max_length=255, verbose_name='ID given by provider', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MixtapeSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('votes', models.IntegerField(default=1)),
                ('mixtape', models.ForeignKey(to='mixtapes.Mixtape')),
                ('song', models.ForeignKey(to='playlists.Song')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='mixtape',
            name='songs',
            field=models.ManyToManyField(to='playlists.Song', through='mixtapes.MixtapeSong'),
        ),
    ]
