__author__ = 'david'

import urllib, json
from flaskext.oauth import OAuth

oauth = OAuth()

class Facebook():
    
    def __init__(self, application_id, application_secret):
        self.oauth = OAuth()
        self.connection = oauth.remote_app('facebook',
                                         base_url='https://graph.facebook.com/',
                                         request_token_url=None,
                                         access_token_url='/oauth/access_token',
                                         authorize_url='https://www.facebook.com/dialog/oauth',
                                         consumer_key=application_id,
                                         consumer_secret=application_secret,
                                         request_token_params={'scope': 'email'})

def get_profile(access_token):
    return json.load(urllib.urlopen(
        "https://graph.facebook.com/me?" +
        urllib.urlencode(dict(access_token=access_token))))