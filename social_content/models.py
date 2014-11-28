#! coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from polymorphic import PolymorphicModel
from positions import PositionField


class Content(PolymorphicModel):
    class Meta:
        verbose_name = _('content')
        ordering = ['-published_at', ]

    identifier = models.CharField(max_length=200, verbose_name=_('identifier'), blank=False, null=True)

    text = models.TextField(verbose_name=_('text'), blank=True, null=True)

    published = models.BooleanField(default=False, verbose_name=_('published'), blank=True)
    published_at = models.DateTimeField(verbose_name=_('published at'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'), blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'), blank=True, null=True)

    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name=_('image URL'))

    image = models.ImageField(blank=True, null=True)

    position = PositionField(verbose_name=_('position'))

    original_url = models.URLField(blank=True, null=True, verbose_name=_('original URL'))

    def __unicode__(self):
        return self.text


class TwitterContent(Content):
    class Meta:
        verbose_name = _('twitter content')
        verbose_name_plural = _('twitter contents')

    number_of_retweets = models.IntegerField(verbose_name=_('number of retweets'), default=0, blank=True, null=True)
    number_of_favourites = models.IntegerField(verbose_name=_('number of favourites'), default=0, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, verbose_name=_('video URL'))


class YoutubeContent(Content):
    class Meta:
        verbose_name = _('youtube content')
        verbose_name_plural = _('youtube contents')

    title = models.CharField(max_length=200, verbose_name=_('title'))

    number_of_views = models.IntegerField(verbose_name=_('number of views'), default=0, blank=True, null=True)
    number_of_comments = models.IntegerField(verbose_name=_('number of comments'), default=0, blank=True, null=True)
    number_of_likes = models.IntegerField(verbose_name=_('number of likes'), default=0, blank=True, null=True)
    number_of_dislikes = models.IntegerField(verbose_name=_('number of dislikes'), default=0, blank=True, null=True)
    duration = models.IntegerField(verbose_name=_('duration'), default=0, blank=True, null=True,
                                   help_text=_('Duration in seconds'))

    def __unicode__(self):
        return self.title


class FacebookContent(Content):
    class Meta:
        verbose_name = _('facebook content')
        verbose_name_plural = _('facebook contents')

    number_of_comments = models.IntegerField(verbose_name=_('number of comments'), default=0, blank=True, null=True)
    number_of_likes = models.IntegerField(verbose_name=_('number of likes'), default=0, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, verbose_name=_('video URL'))