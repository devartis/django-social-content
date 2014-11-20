from django.core.management.base import BaseCommand
from datetime import datetime
from django.utils import timezone
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from django.conf import settings

from social_content.models import YoutubeContent


def prepare_credentials():
    storage = Storage(settings.YOUTUBE_TOKEN_FILE_NAME)
    credentials = storage.get()

    return credentials


def initialize_service():
    http = httplib2.Http()

    credentials = prepare_credentials()

    http = credentials.authorize(http)

    return build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION, http=http)


youtube = initialize_service()


class Command(BaseCommand):

    def handle(self, *args, **options):
        channels_response = youtube.channels().list(
            id=settings.YOUTUBE_CHANNEL_BRAHMA_ID,
            part="contentDetails"
        ).execute()

        for channel in channels_response["items"]:

            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

            playlistitems_list_request = youtube.playlistItems().list(
                playlistId=uploads_list_id,
                part="snippet"
            )

            while playlistitems_list_request:
                playlistitems_list_response = playlistitems_list_request.execute()

                for playlist_item in playlistitems_list_response["items"]:
                    video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                    title = playlist_item["snippet"]["title"]
                    description = playlist_item["snippet"]["description"]

                    videos = youtube.videos().list(id=video_id, part="snippet,statistics,contentDetails").execute()
                    video = videos["items"][0]

                    published_at = video["snippet"]["publishedAt"]
                    published_at = datetime.strptime(published_at[0:10]+' '+published_at[11:19], '%Y-%m-%d %H:%M:%S')
                    published_at = timezone.make_aware(published_at, timezone.get_current_timezone())

                    view_count = video["statistics"]["viewCount"]
                    comment_count = video["statistics"]["commentCount"]
                    like_count = video["statistics"]["likeCount"]
                    thumbnails = videos["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
                    original_url = "https://www.youtube.com/watch?v="+video_id

                    dislike_count = video["statistics"]["dislikeCount"]
                    duration = video["contentDetails"]["duration"]

                    if len(duration) > 5:
                        minutes, secs = duration[2:-1].split('M')
                        duration = int(minutes)*60+int(secs)
                    else:
                        duration = duration[2:-1]

                    try:
                        old_content = YoutubeContent.objects.get(identifier=video_id)
                        old_content.number_of_views = view_count
                        old_content.number_of_comments = comment_count
                        old_content.number_of_likes = like_count
                        old_content.number_of_dislikes = dislike_count
                        old_content.text = description
                        old_content.title = title
                        old_content.save()

                    except YoutubeContent.DoesNotExist:
                        new_content = YoutubeContent(number_of_views=view_count, number_of_comments=comment_count,
                                                     number_of_likes=like_count, number_of_dislikes=dislike_count,
                                                     duration=duration, original_url=original_url, image_url=thumbnails,
                                                     published_at=published_at, text=description, title=title,
                                                     identifier=video_id)
                        new_content.save()

                playlistitems_list_request = youtube.playlistItems().list_next(
                    playlistitems_list_request, playlistitems_list_response)



__author__ = 'guillermo'
