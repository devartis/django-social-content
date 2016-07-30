from django.utils import timezone
from datetime import datetime
import re
from open_facebook import OpenFacebook
import oauth2
import json
import urllib
import urllib2
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from django.core.files.base import ContentFile

from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


from social_content.models import FacebookContent
from social_content.models import TwitterContent
from social_content.models import YoutubeContent


class SocialApi(object):

    def __init__(self, credentials):
        self.credentials = credentials
        self.contents = []

    def update_content(self, new_content):
        try:
            try:
                old_content = new_content.__class__.objects.get(identifier=new_content.identifier)

                content_attrs = {key: value for key, value in vars(new_content).items()
                                if key not in ['id', 'published', 'created_at', 'updated_at', 'image']}

                for attr in content_attrs.keys():
                    setattr(old_content, attr, content_attrs[attr])
                old_content.save()

            except new_content.__class__.DoesNotExist:

                if new_content.image_url:
                    self.get_image(new_content)

                new_content.published = True
                
                    new_content.save()
        except Exception as err:
            print 'Could not save content %s: %s' % (new_content, err)

    def run_flow(self):
        self.get_data()
        self.process_contents()

    def get_image(self, content):

        IMAGE_URL = content.image_url
        response = urllib.urlopen(IMAGE_URL)
        file_name = "%s.jpg" % content.identifier
        content.image.save(file_name, ContentFile(response.read()), save=False)


class FacebookApiExplorer(SocialApi):

    def get_data(self):
        self.graph = OpenFacebook(self.credentials['access_token'])

        feed = self.graph.get('me/posts')

        self.contents = feed["data"]

    def process_contents(self):

            for post in self.contents:

                post_id = post["id"]
                identification = re.split("_", post_id)
                account_id = identification[0]
                post_id = identification[1]

                published_at = post["created_time"]
                published_at = datetime.strptime(published_at[0:10]+' '+published_at[11:19], '%Y-%m-%d %H:%M:%S')
                published_at = timezone.make_aware(published_at, timezone.get_fixed_timezone(0))
                if "link" in post.keys():
                    original_url = post["link"]
                else:
                    original_url = "https://www.facebook.com/"+account_id+"/posts/"+post_id

                def search(parameter):
                    try:
                        return post[parameter]
                    except KeyError:
                        return ""

                def amount(parameter):
                    try:
                        return self.graph.get(post['id']+'/'+parameter, summary='1')['summary']['total_count']
                    except KeyError:
                        return 0

                text = search("message")
                video_url = search("source")
                image_url = search("picture")
                image_id = search("object_id")
                post_type = search("type")
                number_of_likes = amount("likes")
                number_of_comments = amount("comments")

                if image_url and image_id:

                    feed = self.graph.get(image_id)
                    try:
                        if post_type == 'video':
                            image_url = sorted(feed['format'], key=lambda k: k['width'], reverse=True)[0]['picture']

                        else:
                            image_url = sorted(feed['images'], key=lambda k: k['width'], reverse=True)[0]['source']
                    except KeyError:
                        #Error finding image_url
                        pass

                new_content = FacebookContent(identifier=post_id, text=text, published_at=published_at,
                                              image_url=image_url, original_url=original_url,
                                              number_of_comments=number_of_comments, number_of_likes=number_of_likes,
                                              video_url=video_url)

                try:
                    if (text or video_url or image_url) and post_type != 'link':
                        self.update_content(new_content)
                except Exception as err:
                    print 'Could not save content %s: %s' % (new_content, err)


class TwitterApiExplorer(SocialApi):

    def get_data(self):

        consumer = oauth2.Consumer(key=self.credentials['consumer_key'], secret=self.credentials['consumer_secret'])
        access_token = oauth2.Token(key=self.credentials['access_key'], secret=self.credentials['access_secret'])
        client = oauth2.Client(consumer, access_token)

        timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?"

        params = dict(user_id=self.credentials['user_id'], count=self.credentials['tweets_amount'])

        timeline_endpoint += urllib.urlencode(params)

        response, data = client.request(timeline_endpoint)

        self.contents = json.loads(data)

    def process_contents(self):

        for tweet in self.contents:

            tweet_id = tweet["id_str"]
            text = tweet["text"]
            created_at = tweet["created_at"]

            published_at = datetime.strptime(created_at[4:19]+' '+created_at[26:30], '%b %d %H:%M:%S %Y')
            published_at = timezone.make_aware(published_at, timezone.get_fixed_timezone(0))

            retweet_count = tweet["retweet_count"]
            favourite_count = tweet["favorite_count"]
            original_url = "https://twitter.com/"+tweet["user"]["screen_name"]+"/status/"+tweet_id

            try:
                image = tweet["entities"]["media"][0]["media_url_https"]
            except KeyError:
                image = None

            videos_or_urls = []
            for video_or_url in tweet["entities"]["urls"]:
                videos_or_urls.append(video_or_url["expanded_url"])

            new_content = TwitterContent(number_of_retweets=retweet_count, number_of_favourites=favourite_count,
                                         original_url=original_url, image_url=image, published_at=published_at,
                                         text=text, identifier=tweet_id)
            if len(videos_or_urls) > 0:
                    new_content.video_url = videos_or_urls[0]

            self.update_content(new_content)


class YoutubeApiExplorer(SocialApi):

    def prepare_credentials(self):
        storage = Storage(self.credentials['token_file_name'])
        credentials = storage.get()

        # The first time you ask for authorization if you don't have a previous youtube.dat with access_token,
        # the authentication flow must be run
        # To do this you'll need a client_secrets.json and a google project that has access to google youtube api
        # For example: https://console.developers.google.com/project/quilmes-qlub
        # Check that your access_token has a 'refresh_token' so that it will refresh periodically
        # More information in: https://developers.google.com/youtube/v3/getting-started#before-you-start

        # client_secrets example:
        # {
        #       "installed": {
        #         "client_id":"xxxxxxxxx",
        #         "client_secret": "xxxxxxxx",
        #         "redirect_uris": ["http://localhost:8080/"],
        #         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        #         "token_uri": "https://accounts.google.com/o/oauth2/token"
        #       }
        #     }
        # information must be obtained from your google project

        if credentials is None:
            flow = flow_from_clientsecrets('client_secrets.json',
                               message='client_secret is missing',
                               scope="https://www.googleapis.com/auth/youtube.readonly")
            flow.params['approval_prompt'] = 'force'

            credentials = run(flow, storage)

        return credentials

    def initialize_service(self):
        http = httplib2.Http()

        credentials = self.prepare_credentials()

        http = credentials.authorize(http)

        return build(self.credentials['service_name'], self.credentials['version'], http=http)

    def get_data(self):

        self.youtube = self.initialize_service()
        channels_response = self.youtube.channels().list(
            id=self.credentials['channel_id'],
            part="contentDetails"
        ).execute()

        for channel in channels_response["items"]:

            uploads_list_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]

            self.contents = self.youtube.playlistItems().list(
                playlistId=uploads_list_id,
                part="snippet"
            )

    def get_image(self, content):
        quality_list = ['maxresdefault.jpg', 'hqdefault.jpg', 'sddefault.jpg', '0.jpg']
        for quality in quality_list:
            try:
                IMAGE_URL = "http://i.ytimg.com/vi/" + content.identifier + "/" + quality
                response = urllib2.urlopen(IMAGE_URL)
                file_name = "%s.jpg" % content.identifier
                content.image.save(file_name, ContentFile(response.read()), save=False)
                break
            except urllib2.URLError as e:
                pass

    def process_contents(self):
        while self.contents:
            playlistitems_list_response = self.contents.execute()

            for playlist_item in playlistitems_list_response["items"]:
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                title = playlist_item["snippet"]["title"]
                description = playlist_item["snippet"]["description"]

                videos = self.youtube.videos().list(id=video_id, part="snippet,statistics,contentDetails").execute()
                video = videos["items"][0]

                published_at = video["snippet"]["publishedAt"]
                published_at = datetime.strptime(published_at[0:10]+' '+published_at[11:19], '%Y-%m-%d %H:%M:%S')
                published_at = timezone.make_aware(published_at, timezone.get_fixed_timezone(0))

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

                new_content = YoutubeContent(number_of_views=view_count, number_of_comments=comment_count,
                                             number_of_likes=like_count, number_of_dislikes=dislike_count,
                                             duration=duration, original_url=original_url, image_url=thumbnails,
                                             published_at=published_at, text=description, title=title,
                                             identifier=video_id)

                self.update_content(new_content)

            self.contents = self.youtube.playlistItems().list_next(
                self.contents, playlistitems_list_response)


__author__ = 'guillermo'
