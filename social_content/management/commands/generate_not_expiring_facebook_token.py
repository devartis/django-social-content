from django.core.management.base import BaseCommand

from open_facebook import api, OpenFacebook


class Command(BaseCommand):

    def handle(self, app_id, app_secret, user_token, *args, **options):

        # To generate a user_token use https://developers.facebook.com/tools/explorer/
        #   manage_pages permission must be active

        user_token_extended = api.FacebookConnection.request("oauth/access_token?client_id="+app_id+"&client_secret=" +
                                                             app_secret+"&grant_type=fb_exchange_token&fb_exchange_token=" +
                                                             user_token)

        graph = OpenFacebook(user_token_extended["access_token"])

        accounts = graph.get('me/accounts')

        not_expiring_token = accounts["data"][0]["access_token"]

        print not_expiring_token

__author__ = 'guillermo'
