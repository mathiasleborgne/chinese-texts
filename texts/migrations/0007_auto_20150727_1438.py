# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0006_text_chars_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='biography',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='year_birth',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='year_death',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
