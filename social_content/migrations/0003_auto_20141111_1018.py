# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_content', '0002_auto_20140911_1137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['position'], 'verbose_name': 'content'},
        ),
        migrations.AddField(
            model_name='content',
            name='published_at',
            field=models.DateTimeField(null=True, verbose_name='published at', blank=True),
            preserve_default=True,
        ),
    ]
