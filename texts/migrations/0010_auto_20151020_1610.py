# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0009_auto_20151019_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.SlugField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='slug',
            field=models.SlugField(max_length=42, null=True),
        ),
    ]
