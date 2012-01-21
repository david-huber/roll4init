import os, re, urllib, urlparse

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from persist import mongo
from facebook import Facebook


MONGO_URL = os.environ.get("MONGOLAB_URI", "mongodb://localhost:27017/test_database")

def parseMongoConfig():
    mongoUrl = os.environ.get("MONGOLAB_URI", "mongodb://:@localhost:27017/test_database")
    match = re.match(r"mongodb://(.*):(.*)@(.*):(.*)/(.*)", mongoUrl)
    return match.groups()

MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DB = parseMongoConfig()

try:
    import debug
    DEBUG = True
except ImportError:
    debug = {}

SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", 'development key')
FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET")
facebook = Facebook(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)

app = Flask(__name__)
app.config.from_object(__name__)

authz = facebook.connection

@authz.tokengetter
def get_access_token():
    return session.get('access_token')

@app.before_request
def before_request():
    g.mongo = mongo.connect_db(app)

@app.teardown_request
def teardown_request(exception):
    g.mongo.close()

@app.route("/")
def show_entries():
    entries = g.mongo.database.entries.find()
    return render_template('show_entries.html', entries=entries)

@app.route('/login')
def login():
    return authz.authorize(callback=request.url_root[:-1] + url_for('authorized'))

@app.route('/authorized')
@authz.authorized_handler
def authorized(resp):
    next_url = request.args.get('next') or url_for('show_entries')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    facebook.authorize(resp)

    flash('You were logged in')
    return redirect(next_url)

@app.route('/logout')
def logout():
    facebook.clear()
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)