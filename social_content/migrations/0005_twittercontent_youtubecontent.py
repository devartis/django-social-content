# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_content', '0004_auto_20141113_1444'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterContent',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social_content.Content')),
                ('number_of_retweets', models.IntegerField(default=0, null=True, verbose_name='number of retweets', blank=True)),
                ('number_of_favourites', models.IntegerField(default=0, null=True, verbose_name='number of favourites', blank=True)),
                ('video_url', models.URLField(null=True, verbose_name='video URL', blank=True)),
            ],
            options={
                'verbose_name': 'twitter content',
            },
            bases=('social_content.content',),
        ),
        migrations.CreateModel(
            name='YoutubeContent',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social_content.Content')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('number_of_views', models.IntegerField(default=0, null=True, verbose_name='number of views', blank=True)),
                ('number_of_comments', models.IntegerField(default=0, null=True, verbose_name='number of comments', blank=True)),
                ('number_of_likes', models.IntegerField(default=0, null=True, verbose_name='number of likes', blank=True)),
                ('number_of_dislikes', models.IntegerField(default=0, null=True, verbose_name='number of dislikes', blank=True)),
                ('duration', models.IntegerField(default=0, help_text='Duration in seconds', null=True, verbose_name='duration', blank=True)),
            ],
            options={
                'verbose_name': 'youtube content',
            },
            bases=('social_content.content',),
        ),
    ]
