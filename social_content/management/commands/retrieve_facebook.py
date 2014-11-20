from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
import re
from django.conf import settings
from open_facebook import OpenFacebook
from social_content.models import FacebookContent



class Command(BaseCommand):

    def handle(self, *args, **options):

        graph = OpenFacebook(settings.FACEBOOK_ACCESS_TOKEN)
        graph.get('me/feed')

        feed = graph.get('me/feed')

        posts = feed["data"]

        for post in posts:

            post_id = post["id"]
            identification = re.split("_",post_id)
            account_id = identification[0]
            post_id = identification[1]

            published_at = post["created_time"]
            published_at = datetime.strptime(published_at[0:10]+' '+published_at[11:19], '%Y-%m-%d %H:%M:%S')
            published_at = timezone.make_aware(published_at, timezone.get_current_timezone())

            original_url = "https://www.facebook.com/"+account_id+"/posts/"+post_id

            def search(parameter):
                try:
                    return post[parameter]
                except KeyError:
                    return ""

            def amount(parameter):
                try:
                    return len(post[parameter]["data"])
                except KeyError:
                    return 0

            text = search("message")
            video_url = search("source")
            image_url = search("picture")
            number_of_likes = amount("likes")
            number_of_comments = amount("comments")

            if text or video_url or image_url:
                try:
                    old_content = FacebookContent.objects.get(identifier=post_id)
                    old_content.text = text
                    old_content.image_url = image_url
                    old_content.number_of_comments = number_of_comments
                    old_content.number_of_likes = number_of_likes
                    old_content.video_url = video_url
                    old_content.save()

                except FacebookContent.DoesNotExist:
                    new_content = FacebookContent(identifier=post_id, text=text, published_at=published_at,
                                                  image_url=image_url, original_url=original_url,
                                                  number_of_comments=number_of_comments, number_of_likes=number_of_likes,
                                                  video_url=video_url)

                    new_content.save()

__author__ = 'guillermo'
