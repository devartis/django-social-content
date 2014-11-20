# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('text', models.TextField(null=True, verbose_name='text', blank=True)),
                ('published', models.BooleanField(default=False, verbose_name='published')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at', null=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'content/', null=True, verbose_name='image', blank=True)),
                ('number_of_views', models.IntegerField(default=0, null=True, verbose_name='number of views', blank=True)),
                ('number_of_comments', models.IntegerField(default=0, null=True, verbose_name='number of comments', blank=True)),
                ('number_of_likes', models.IntegerField(default=0, null=True, verbose_name='number of likes', blank=True)),
                ('original_url', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
