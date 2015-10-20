# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20151019_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='client_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='client_secret',
        ),
        migrations.RemoveField(
            model_name='user',
            name='playlists',
        ),
        migrations.RemoveField(
            model_name='user',
            name='spotify_username',
        ),
    ]
