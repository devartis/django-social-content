from django.core.management.base import BaseCommand
from django.conf import settings

from api_explorer import TwitterApiExplorer


class Command(BaseCommand):

    def handle(self, *args, **options):

        credentials = {'consumer_key': settings.TWITTER_CONSUMER_KEY,
                       'consumer_secret': settings.TWITTER_CONSUMER_SECRET, 'access_key': settings.TWITTER_ACCESS_KEY,
                       'access_secret': settings.TWITTER_ACCESS_SECRET, 'user_id': settings.TWITTER_USER_ID,
                       'tweets_amount': settings.TWEETS_AMOUNT}

        twitter_api_explorer = TwitterApiExplorer(credentials)

        twitter_api_explorer.run_flow()

__author__ = 'guillermo'
