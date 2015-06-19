# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='text',
            old_name='auteur',
            new_name='author',
        ),
    ]
