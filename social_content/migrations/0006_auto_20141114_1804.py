# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_twittercontent_youtubecontent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['-published_at'], 'verbose_name': 'content'},
        ),
        migrations.AlterModelOptions(
            name='twittercontent',
            options={'verbose_name': 'twitter content', 'verbose_name_plural': 'twitter contents'},
        ),
        migrations.AlterModelOptions(
            name='youtubecontent',
            options={'verbose_name': 'youtube content', 'verbose_name_plural': 'youtube contents'},
        ),
    ]
