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

class FromDocumentTest(unittest.TestCase):

    def test_fighterFromNoneDocumentReturnsNone(self):
        fighter = fighter_from_document(None)
        self.assertIsNone(fighter)

    def test_fighterFromDictWithIdSetsId(self):
        fighter = fighter_from_document({"_id" : "1234"})
        self.assertEqual(fighter.id, "1234")

    def test_fighterFromDictWithNameSetsJustName(self):
        fighter = fighter_from_document({"name" : "Damakos"})
        self.assertEqual(fighter.id, None)
        self.assertEqual(fighter.name, "Damakos")

    def test_fighterFromDictWithNameAndIdSetsBoth(self):
        fighter = fighter_from_document({"name" : "Forel", "_id" : "555"})
        self.assertEqual(fighter.id, "555")
        self.assertEqual(fighter.name, "Forel")

    def test_fighterFromDictWithAllValuesSetIsCompletelyConstructed(self):
        fighter = fighter_from_document({"name" : "Soraya", "_id" : "556", "initiative" : "1d20+11"})
        self.assertEqual(fighter.id, "556")
        self.assertEqual(fighter.name, "Soraya")
        self.assertEqual(fighter.initiative, Pool(dice=[Die(sides=20, showing=1)], modifier=11))

    def test_fighterFromBlankDictJustHasD20Init(self):
        fighter = fighter_from_document({})
        self.assertEqual(fighter.id, None)
        self.assertEqual(fighter.name, None)
        self.assertEqual(fighter.initiative, Pool(dice=[Die(sides=20)]))

    def test_fighterWithRolledInitHasProperlySummedInit(self):
        fighter = fighter_from_document({"name" : "EvilPlugh", "initiative" : "1d20+4 (23)"})
        self.assertEqual(fighter.id, None)
        self.assertEqual(fighter.name, "EvilPlugh")
        self.assertEqual(fighter.initiative, Pool(dice=[Die(sides=20, showing=19)], modifier=4, rolled=True))