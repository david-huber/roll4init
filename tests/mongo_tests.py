import unittest
import pymongo
from persist import *
from mock import patch, Mock, MagicMock

class MongoDBTest(unittest.TestCase):

    def setUp(self):
        self.appStub = Mock()
        self.appStub.config = { 'MONGO_URL' : 'someUrl', 'MONGO_DB' : 'someDB' }

    def configure_connection_mock(self, connection_mock):
        connection_mock.return_value = MagicMock()
        connection_mock.return_value.__getitem__.return_value = 'databaseValue'
        connection_mock.return_value.close = MagicMock()

    @patch.object(pymongo, 'Connection')
    def test_initConnectsToAppUrl(self, connection_mock):
        self.configure_connection_mock(connection_mock)
        MongoDB(self.appStub)
        connection_mock.assert_called_once_with('someUrl')

    @patch.object(pymongo, 'Connection')
    def test_initGetsDatabase(self, connection_mock):
        self.configure_connection_mock(connection_mock)
        db = MongoDB(self.appStub)
        self.assertEqual(db.database, 'databaseValue')

    @patch.object(pymongo, 'Connection')
    def test_closeClosesConnection(self, connection_mock):
        self.configure_connection_mock(connection_mock)
        db = MongoDB(self.appStub)
        db.close()
        connection_mock.return_value.close.assert_called_once()
