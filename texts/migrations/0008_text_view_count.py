# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0007_auto_20150727_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
