# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0004_auto_20150630_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='year_birth',
        ),
        migrations.RemoveField(
            model_name='author',
            name='year_death',
        ),
    ]
