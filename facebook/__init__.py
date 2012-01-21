__author__ = 'david'

import urllib, json
from flask import session
from flaskext.oauth import OAuth

oauth = OAuth()

class Facebook():
    
    graphApiUrl = 'https://graph.facebook.com/'
    
    def __init__(self, application_id, application_secret):
        self.oauth = OAuth()
        self.connection = oauth.remote_app('facebook',
                                         base_url=Facebook.graphApiUrl,
                                         request_token_url=None,
                                         access_token_url='/oauth/access_token',
                                         authorize_url='https://www.facebook.com/dialog/oauth',
                                         consumer_key=application_id,
                                         consumer_secret=application_secret,
                                         request_token_params={'scope': 'email'})

    def authorize(self, resp):
        session['logged_in'] = True
        session['access_token'] = resp['access_token']
        profile = self._get_profile(session['access_token'])
        session['fb_id'] = profile["id"]
        session['fb_name'] = profile["name"]

    def clear(self):
        session.pop('logged_in', None)
        session.pop('access_token', None)
        session.pop('fb_id', None)
        session.pop('fb_name', None)

    def _get_profile(self, access_token):
        return json.load(urllib.urlopen(
            Facebook.graphApiUrl + "me?" +
            urllib.urlencode(dict(access_token=access_token))))