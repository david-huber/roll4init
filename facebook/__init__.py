__author__ = 'david'

import urllib, json
from flask import session
from flaskext.oauth import OAuth

oauth = OAuth()

class Facebook():
    
    graphApiUrl = 'https://graph.facebook.com/'
    
    def __init__(self, application_id, application_secret, dm_id):
        self.oauth = OAuth()
        self.connection = oauth.remote_app('facebook',
                                         base_url=Facebook.graphApiUrl,
                                         request_token_url=None,
                                         access_token_url='/oauth/access_token',
                                         authorize_url='https://www.facebook.com/dialog/oauth',
                                         consumer_key=application_id,
                                         consumer_secret=application_secret,
                                         request_token_params={'scope': 'email'})
        self.dm_id = dm_id

    def authorize(self, resp):
        access_token = resp['access_token']
        profile = self._get_profile(access_token)

        if profile["id"] == self.dm_id:
            session['dm'] = True
        elif self._is_player(access_token):
            session['dm'] = False
        else:
            return False


        session['logged_in'] = True
        session['access_token'] = access_token
        session['fb_id'] = profile["id"]
        session['fb_name'] = profile["name"]
        session['email'] = profile["email"]

        return True

    def _is_player(self, access_token):
        friendResp = self._get_friends(access_token)
        friends = friendResp["data"]
        friend_of_dm = False
        while (len(friends) > 0 and not friend_of_dm):
            friend_of_dm = any(map(lambda f: f["id"] == self.dm_id, friends))
            if not friend_of_dm:
                print(friendResp)
                friendResp = self._next(friendResp["paging"]["next"])
                friends = friendResp["data"]

        return friend_of_dm



    def clear(self):
        session.pop('logged_in', None)
        session.pop('access_token', None)
        session.pop('fb_id', None)
        session.pop('fb_name', None)
        session.pop('email', None)
        session.pop('dm', None)

    def _get_profile(self, access_token):
        return self._load_json(access_token, Facebook.graphApiUrl + "me")

    def _get_friends(self, access_token):
        return self._load_json(access_token, Facebook.graphApiUrl + "me/friends")

    def _get_dm(self, access_token):
        return self._load_json(access_token, Facebook.graphApiUrl + self.dm_id)

    def _load_json(self, access_token, url):
        return json.load(urllib.urlopen(url + "?" + urllib.urlencode(dict(access_token=access_token))))

    def _next(self, url):
        return json.load(urllib.urlopen(url))