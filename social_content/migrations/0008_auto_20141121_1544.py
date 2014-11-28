# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_content', '0007_facebookcontent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facebookcontent',
            options={'verbose_name': 'facebook content', 'verbose_name_plural': 'facebook contents'},
        ),
        migrations.AddField(
            model_name='content',
            name='image',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
