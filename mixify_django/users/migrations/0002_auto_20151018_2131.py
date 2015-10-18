# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='client_id',
            field=models.CharField(max_length=255, verbose_name='ClientID', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='client_secret',
            field=models.CharField(max_length=255, verbose_name='ClientSecret', blank=True),
        ),
    ]
