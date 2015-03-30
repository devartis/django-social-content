from django.core.management.base import BaseCommand
from social_content.models import FacebookContent
import urllib
from django.core.files.base import ContentFile


class Command(BaseCommand):

    def handle(self, *args, **options):

        facebook_contents = FacebookContent.objects.all()

        for content in facebook_contents:
            if content.image_url:
                IMAGE_URL = content.image_url
                response = urllib.urlopen(IMAGE_URL)
                file_name = "%s.jpg" % content.identifier
                content.image.save(file_name, ContentFile(response.read()), save=False)
                content.save()

__author__ = 'guillermo'