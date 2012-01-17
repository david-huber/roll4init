__author__ = 'david'

import urllib, json

def get_profile(access_token):
    return json.load(urllib.urlopen(
        "https://graph.facebook.com/me?" +
        urllib.urlencode(dict(access_token=access_token))))