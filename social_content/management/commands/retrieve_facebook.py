from django.core.management.base import BaseCommand
from django.conf import settings
from api_explorer import FacebookApiExplorer


class Command(BaseCommand):

    def handle(self, *args, **options):

        credentials = {'access_token': settings.FACEBOOK_ACCESS_TOKEN}

        facebook_api_explorer = FacebookApiExplorer(credentials)

        facebook_api_explorer.run_flow()

__author__ = 'guillermo'
