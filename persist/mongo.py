from pymongo import Connection

def connect_db(app):
    return Connection(app.config['MONGO_URL'])

class MongoDB:

    def __init__(self, app):
        self.connection = Connection(app.config['MONGO_URL'])
        self.database = self.connection[app.config['MONGO_DB']]

    def close(self):
        self.connection.close()