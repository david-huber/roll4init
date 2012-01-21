import unittest
from persist import *
from tracker import *
from mock import Mock
from dice import *

class FighterRepositoryTest(unittest.TestCase):

    def test_saveUnidentifiedFighterToCollection(self):
        connection_mock = Mock()
        connection_mock.save = Mock()
        repo = FighterRepository(connection_mock)
        repo.save(Fighter())
        connection_mock.save.assert_called_once_with({ "initiative" : "1d20" })

    def test_saveUnidentifiedFastFighterToCollection(self):
        connection_mock = Mock()
        connection_mock.save = Mock()
        repo = FighterRepository(connection_mock)
        repo.save(Fighter(initiative=Pool(dice=[Die(sides=20)], modifier=20)))
        connection_mock.save.assert_called_once_with({ "initiative" : "1d20+20" })

    def test_saveNewDamakosToCollection(self):
        connection_mock = Mock()
        connection_mock.save = Mock()
        repo = FighterRepository(connection_mock)
        repo.save(Fighter(name="Damakos"))
        connection_mock.save.assert_called_once_with({ "initiative" : "1d20", "name" : "Damakos" })

    def test_saveExistingForelToCollection(self):
        connection_mock = Mock()
        connection_mock.save = Mock()
        repo = FighterRepository(connection_mock)
        repo.save(Fighter(name="Forel", id="1"))
        connection_mock.save.assert_called_once_with({ "initiative" : "1d20", "name" : "Forel", "_id" : "1" })