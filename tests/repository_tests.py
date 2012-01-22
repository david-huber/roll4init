import unittest
from persist import *
from tracker import *
from mock import Mock
from dice import *

class FighterRepositoryTest(unittest.TestCase):

    def create_connection_mock(self):
        connection_mock = Mock()
        connection_mock.save = Mock()
        connection_mock.remove = Mock()
        connection_mock.find_one = Mock()
        return connection_mock

    def test_saveUnidentifiedFighterToCollection(self):
        connection_mock = self.create_connection_mock()
        repo = FighterRepository(connection_mock)
        repo.save(Fighter())
        connection_mock.save.assert_called_once_with({ "initiative" : "1d20" })

    def test_saveUnidentifiedFastFighterToCollection(self):
        connection_mock = self.create_connection_mock()
        repo = FighterRepository(connection_mock)
        repo.save(Fighter(initiative=Pool(dice=[Die(sides=20)], modifier=20)))
        connection_mock.save.assert_called_once_with({ "initiative" : "1d20+20" })

    def test_saveNewDamakosToCollection(self):
        connection_mock = self.create_connection_mock()
        repo = FighterRepository(connection_mock)
        repo.save(Fighter(name="Damakos"))
        connection_mock.save.assert_called_once_with({ "initiative" : "1d20", "name" : "Damakos" })

    def test_saveExistingForelToCollection(self):
        connection_mock = self.create_connection_mock()
        repo = FighterRepository(connection_mock)
        repo.save(Fighter(name="Forel", id="1"))
        connection_mock.save.assert_called_once_with({ "initiative" : "1d20", "name" : "Forel", "_id" : "1" })

    def test_removeUnidentifiedFighterRaisesValueError(self):
        connection_mock = self.create_connection_mock()
        repo = FighterRepository(connection_mock)
        self.assertRaises(ValueError, repo.remove, Fighter())

    def test_removeNewDamakosFromCollection(self):
        connection_mock = self.create_connection_mock()
        repo = FighterRepository(connection_mock)
        repo.remove(Fighter(name="Damakos"))
        connection_mock.remove.assert_called_once_with({ "name" : "Damakos" })

    def test_removeExistingForelFromCollection(self):
        connection_mock = self.create_connection_mock()
        repo = FighterRepository(connection_mock)
        repo.remove(Fighter(name="Forel", id="1"))
        connection_mock.remove.assert_called_once_with({ "name" : "Forel", "_id" : "1" })
    
    def test_findOneFromCollection(self):
        connection_mock = self.create_connection_mock()
        connection_mock.find_one.return_value = "Whatever"
        repo = FighterRepository(connection_mock)
        result = repo.find_one()
        self.assertEquals(result, "Whatever")
        connection_mock.find_one.assert_called_once_with(spec=None)

    def test_findOneWithSpecFromCollection(self):
        connection_mock = self.create_connection_mock()
        connection_mock.find_one.return_value = "Whatever"
        repo = FighterRepository(connection_mock)
        result = repo.find_one(spec="Something")
        self.assertEquals(result, "Whatever")
        connection_mock.find_one.assert_called_once_with(spec="Something")