from django.core.management.base import BaseCommand

from open_facebook import OpenFacebook
import httplib2

class Command(BaseCommand):

    def handle(self, app_id, app_secret, facebook_page_id, user_token, *args, **options):

        # To generate a user_token use https://developers.facebook.com/tools/explorer/
        #   Select your application and Get Access Token
        #   manage_pages in Extended Permissions must be enabled for this token

        # facebook_page_id can also be obtained from https://developers.facebook.com/tools/explorer/
        # Query for 'me/accounts' and look for the id of your facebook page
        # Another way to find the id is using http://findmyfacebookid.com/
        # There you will only have to enter the url of your page to get the page id

        h = httplib2.Http("")
        resp, content = h.request("https://graph.facebook.com/oauth/access_token?client_id"
                                  "="+app_id+"&client_secret="+app_secret+"&grant_type=fb_excha"
                                  "nge_token&fb_exchange_token="+user_token, "POST")
        
        user_token_extended = content[13:]

        graph = OpenFacebook(user_token_extended)

        accounts = graph.get('me/accounts')

        page = filter(lambda page: page['id'] == facebook_page_id, accounts["data"])[0]

        not_expiring_token = page["access_token"]

        print not_expiring_token

__author__ = 'guillermo'