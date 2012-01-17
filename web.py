import os, re, urllib, cgi, urlparse

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from persist import mongo
from facebook import get_profile

MONGO_URL = os.environ.get("MONGOLAB_URI", "mongodb://localhost:27017/test_database")

def parseMongoConfig():

    #mongodb://username:password@host:port/database
    mongoUrl = os.environ.get("MONGOLAB_URI", "mongodb://:@localhost:27017/test_database")
    match = re.match(r"mongodb://(.*):(.*)@(.*):(.*)/(.*)", mongoUrl)
    return match.groups()

def get_secret_app_id():
    import secrets
    return secrets.facebook_app_id

def get_secret_app_secret():
    import secrets
    return secrets.facebook_app_secret

MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DB = parseMongoConfig()

USERNAME = "DAVE"
PASSWORD = "tacos"
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", 'development key')
DEBUG = True

FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID", get_secret_app_id())

FACEBOOK_APP_SECRET = os.environ.get("FACEBOOK_APP_SECRET", get_secret_app_secret())

app = Flask(__name__)
app.config.from_object(__name__)

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

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    entry = {'title': request.form['title'],
             'text' : request.form['text'] }

    g.mongo.database.entries.insert(entry)
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/facelogin', methods=['GET', 'POST'])
def face_login():
    args = dict(client_id=app.config["FACEBOOK_APP_ID"], redirect_uri=request.base_url)
    verification_code = request.args.get("code", None)
    if verification_code:

        args["client_secret"] = app.config["FACEBOOK_APP_SECRET"]
        args["code"] = verification_code
        fb_response = urllib.urlopen(
            "https://graph.facebook.com/oauth/access_token?" +
            urllib.urlencode(args)).read()
        fb_response = urlparse.parse_qs(fb_response)

        access_tokens = fb_response.get("access_token", None)
        if access_tokens and len(access_tokens) > 0:
            access_token = access_tokens[-1]

            profile = get_profile(access_token)
            session['fb_id'] = profile["id"]
            session['fb_name'] = profile["name"]
            session['logged_in'] = True

            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else:
            flash('Invalid access token')
            return redirect(url_for('show_entries'))

    else:
        return redirect("https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('fb_id', None)
    session.pop('fb_name', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)