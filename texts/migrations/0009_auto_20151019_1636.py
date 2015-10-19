# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0008_text_view_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='text',
            options={'ordering': ['chars_data', 'content_pinyin']},
        ),
        migrations.AddField(
            model_name='author',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
