import os
import re

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from persist import mongo

MONGO_URL = os.environ.get("MONGOLAB_URI", "mongodb://localhost:27017/test_database")

def parseMongoConfig():

    #mongodb://username:password@host:port/database
    mongoUrl = os.environ.get("MONGOLAB_URI", "mongodb://:@localhost:27017/test_database")
    match = re.match(r"mongodb://(.*):(.*)@(.*):(.*)/(.*)", mongoUrl)
    return match.groups()


MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DB = parseMongoConfig()

USERNAME = "DAVE"
PASSWORD = "tacos"
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", 'development key')
DEBUG = (SECRET_KEY != "development key")


app = Flask(__name__)
app.config.from_object(__name__)




@app.before_request
def before_request():
    g.mongo = mongo.connect_db(app)

@app.teardown_request
def teardown_request(exception):
    g.mongo.close()
    pass

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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)