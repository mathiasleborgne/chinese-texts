# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0005_auto_20150727_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='chars_data',
            field=models.TextField(null=True),
        ),
    ]
