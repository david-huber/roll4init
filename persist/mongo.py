import pymongo

__all__ = ['connect_db', 'MongoDB']

def connect_db(app):
    return MongoDB(app)

class MongoDB:

    def __init__(self, app):
        self.connection = pymongo.Connection(app.config['MONGO_URL'])
        self.database = self.connection[app.config['MONGO_DB']]

    def close(self):
        self.connection.close()