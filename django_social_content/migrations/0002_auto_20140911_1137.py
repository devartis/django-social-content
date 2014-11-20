# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'verbose_name': 'content'},
        ),
        migrations.AddField(
            model_name='content',
            name='position',
            field=positions.fields.PositionField(default=-1, verbose_name='position'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='original_url',
            field=models.URLField(null=True, verbose_name='original URL', blank=True),
        ),
    ]
