# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('social_content', '0009_auto_20141127_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='identifier',
            field=models.CharField(max_length=2500, null=True, verbose_name='identifier'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='image_url',
            field=models.URLField(max_length=2500, null=True, verbose_name='image URL', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='original_url',
            field=models.URLField(max_length=2500, null=True, verbose_name='original URL', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_social_content.content_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='position',
            field=positions.fields.PositionField(default=-1, verbose_name='position'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='text',
            field=models.TextField(max_length=2500, null=True, verbose_name='text', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebookcontent',
            name='video_url',
            field=models.URLField(max_length=2500, null=True, verbose_name='video URL', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittercontent',
            name='video_url',
            field=models.URLField(max_length=2500, null=True, verbose_name='video URL', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='youtubecontent',
            name='title',
            field=models.CharField(max_length=2500, verbose_name='title'),
            preserve_default=True,
        ),
    ]
