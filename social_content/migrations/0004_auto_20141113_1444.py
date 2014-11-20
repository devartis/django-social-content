# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('content', '0003_auto_20141111_1018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['published_at'], 'verbose_name': 'content'},
        ),
        migrations.RemoveField(
            model_name='content',
            name='image',
        ),
        migrations.RemoveField(
            model_name='content',
            name='number_of_comments',
        ),
        migrations.RemoveField(
            model_name='content',
            name='number_of_likes',
        ),
        migrations.RemoveField(
            model_name='content',
            name='number_of_views',
        ),
        migrations.RemoveField(
            model_name='content',
            name='title',
        ),
        migrations.AddField(
            model_name='content',
            name='identifier',
            field=models.CharField(max_length=200, null=True, verbose_name='identifier'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='image_url',
            field=models.URLField(null=True, verbose_name='image URL', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name=b'polymorphic_content.content_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
