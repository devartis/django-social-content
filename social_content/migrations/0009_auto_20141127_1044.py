# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20141121_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image_url',
            field=models.URLField(max_length=500, null=True, verbose_name='image URL', blank=True),
        ),
    ]
