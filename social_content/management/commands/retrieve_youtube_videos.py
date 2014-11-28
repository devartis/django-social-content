from django.core.management.base import BaseCommand
from django.conf import settings

from api_explorer import YoutubeApiExplorer


class Command(BaseCommand):

    def handle(self, *args, **options):

        credentials = {'channel_id': settings.YOUTUBE_CHANNEL_BRAHMA_ID,
                       'token_file_name': settings.YOUTUBE_TOKEN_FILE_NAME,
                       'service_name': settings.YOUTUBE_API_SERVICE_NAME,
                       'version': settings.YOUTUBE_API_VERSION}

        youtube_api_explorer = YoutubeApiExplorer(credentials)

        youtube_api_explorer.run_flow()

__author__ = 'guillermo'
