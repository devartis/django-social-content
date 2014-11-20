from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from django.conf import settings

import oauth2
import json
import urllib

from content.models import TwitterContent


class Command(BaseCommand):

    def handle(self, *args, **options):

        consumer = oauth2.Consumer(key=settings.TWITTER_CONSUMER_KEY, secret=settings.TWITTER_CONSUMER_SECRET)
        access_token = oauth2.Token(key=settings.TWITTER_ACCESS_KEY, secret=settings.TWITTER_ACCESS_SECRET)
        client = oauth2.Client(consumer, access_token)

        timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?"

        # amount of tweets neeeded (max is 3200)
        params = dict(user_id=settings.TWITTER_USER_ID, count=40)

        timeline_endpoint += urllib.urlencode(params)

        response, data = client.request(timeline_endpoint)

        tweets = json.loads(data)

        for tweet in tweets:

            tweet_id = tweet["id_str"]
            text = tweet["text"]
            created_at = tweet["created_at"]
            published_at = datetime.strptime(created_at[4:19]+' '+created_at[26:30], '%b %d %H:%M:%S %Y')
            published_at = timezone.make_aware(published_at, timezone.get_current_timezone())

            retweet_count = tweet["retweet_count"]
            favourite_count = tweet["favorite_count"]
            original_url = "https://twitter.com/"+tweet["user"]["screen_name"]+"/status/"+tweet_id

            try:
                image = tweet["entities"]["media"][0]["media_url_https"]
            except KeyError:
                image = None

            videos_or_urls = []
            for video_or_url in tweet["entities"]["urls"]:
                videos_or_urls.append(video_or_url["expanded_url"])  # videos and any other urls?

            try:
                old_content = TwitterContent.objects.get(identifier=tweet_id)
                old_content.number_of_retweets = retweet_count
                old_content.number_of_favourites = favourite_count
                old_content.save()

            except TwitterContent.DoesNotExist:
                new_content = TwitterContent(number_of_retweets=retweet_count, number_of_favourites=favourite_count,
                                             original_url=original_url, image_url=image, published_at=published_at,
                                             text=text, identifier=tweet_id)
                if len(videos_or_urls) > 0:
                    new_content.video_url = videos_or_urls[0]

                new_content.save()


__author__ = 'guillermo'
