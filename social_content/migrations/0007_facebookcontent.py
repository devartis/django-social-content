# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_content', '0006_auto_20141114_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookContent',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social_content.Content')),
                ('number_of_comments', models.IntegerField(default=0, null=True, verbose_name='number of comments', blank=True)),
                ('number_of_likes', models.IntegerField(default=0, null=True, verbose_name='number of likes', blank=True)),
                ('video_url', models.URLField(null=True, verbose_name='video URL', blank=True)),
            ],
            options={
                'verbose_name': 'facebook content',
            },
            bases=('content.content',),
        ),
    ]
