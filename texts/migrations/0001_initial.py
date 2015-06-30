# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_chinese', models.CharField(max_length=42)),
                ('name_pinyin', models.CharField(max_length=42)),
                ('year_birth', models.IntegerField(null=True)),
                ('year_death', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_english', models.CharField(max_length=100)),
                ('title_chinese', models.CharField(max_length=100)),
                ('content_english', models.TextField(null=True)),
                ('content_chinese', models.TextField(null=True)),
                ('date_release', models.DateTimeField(auto_now_add=True, verbose_name=b'Release Date')),
                ('date_writing', models.DateTimeField(null=True, verbose_name=b'Writing Date')),
                ('auteur', models.ForeignKey(to='texts.Author')),
            ],
        ),
    ]
