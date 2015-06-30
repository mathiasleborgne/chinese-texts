# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0003_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='text',
            old_name='content_english',
            new_name='content_english',
        ),
        migrations.RenameField(
            model_name='text',
            old_name='title_english',
            new_name='title_english',
        ),
        migrations.AddField(
            model_name='text',
            name='content_pinyin',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='title_pinyin',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
