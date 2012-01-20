import unittest
import pymongo
from persist import *
from mock import patch, Mock, MagicMock

class MongoDBTest(unittest.TestCase):


    def setUp(self):
        self.appStub = Mock()
        self.appStub.config = { 'MONGO_URL' : 'someUrl', 'MONGO_DB' : 'someDB' }


    @patch.object(pymongo, 'Connection')
    def test_initConnectsToAppUrl(self, connectionMock):
        connectionMock.return_value = MagicMock()
        connectionMock.return_value['someDB'] = 'whatever'
        MongoDB(self.appStub)
        connectionMock.assert_called_once_with('someUrl')

    @patch.object(pymongo, 'Connection')
    def test_initGetsDatabase(self, connectionMock):
        connectionMock.return_value = MagicMock()
        connectionMock.return_value.__getitem__.return_value = 'databaseValue'
        db = MongoDB(self.appStub)
        self.assertEqual(db.database, 'databaseValue')