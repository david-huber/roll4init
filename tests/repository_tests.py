import unittest
from persist import *
from tracker import *
from mock import Mock, MagicMock, sentinel, patch
from dice import *

class FighterRepositoryTest(unittest.TestCase):

    def setUp(self):
        self.connection_mock = self.create_connection_mock()
        self.repository = FighterRepository(self.connection_mock)

    def create_connection_mock(self):
        connection_mock = Mock()
        connection_mock.save = Mock()
        connection_mock.remove = Mock()
        connection_mock.find = Mock()
        connection_mock.find_one = Mock()
        return connection_mock

    def test_saveUnidentifiedFighterToCollection(self):
        self.repository.save(Fighter())
        self.connection_mock.save.assert_called_once_with({ "initiative" : "1d20" })

    def test_saveUnidentifiedFastFighterToCollection(self):
        self.repository.save(Fighter(initiative=Pool(dice=[Die(sides=20)], modifier=20)))
        self.connection_mock.save.assert_called_once_with({ "initiative" : "1d20+20" })

    def test_saveNewDamakosToCollection(self):
        self.repository.save(Fighter(name="Damakos"))
        self.connection_mock.save.assert_called_once_with({ "initiative" : "1d20", "name" : "Damakos" })

    def test_saveExistingForelToCollection(self):
        self.repository.save(Fighter(name="Forel", id="1"))
        self.connection_mock.save.assert_called_once_with({ "initiative" : "1d20", "name" : "Forel", "_id" : "1" })

    def test_removeUnidentifiedFighterRaisesValueError(self):
        self.assertRaises(ValueError, self.repository.remove, Fighter())

    def test_removeNewDamakosFromCollection(self):
        self.repository.remove(Fighter(name="Damakos"))
        self.connection_mock.remove.assert_called_once_with({ "name" : "Damakos" })

    def test_removeExistingForelFromCollection(self):
        self.repository.remove(Fighter(name="Forel", id="1"))
        self.connection_mock.remove.assert_called_once_with({ "name" : "Forel", "_id" : "1" })

    @patch.object(repository, 'fighter_from_document')
    def test_findWithNoArgumentsCallsToCollection(self, fromPatch):
        self.connection_mock.find.return_value = [sentinel.find_object]
        fromPatch.return_value = sentinel.fighter_object
        fighters = self.repository.find()
        self.connection_mock.find.assert_called_once()
        fromPatch.assert_called_once_with(sentinel.find_object)
        self.assertEqual(fighters, [sentinel.fighter_object])

    @patch.object(repository, 'fighter_from_document')
    def test_findWithArgumentsCallsToCollection(self, fromPatch):
        self.connection_mock.find.return_value = [sentinel.find_object, sentinel.find_object]
        fromPatch.return_value = sentinel.fighter_object
        fighters = self.repository.find(something='x', something_else=1)
        self.connection_mock.find.assert_called_once(something='x', something_else=1)
        fromPatch.assert_called_with(sentinel.find_object)
        self.assertEqual(fromPatch.call_count, 2)
        self.assertEqual(fighters, [sentinel.fighter_object, sentinel.fighter_object])

    @patch.object(repository, 'fighter_from_document')
    def test_findOneWithNoArgumentsCallsToCollection(self, fromPatch):
        self.connection_mock.find_one.return_value = sentinel.find_object
        fromPatch.return_value = sentinel.fighter_object
        fighters = self.repository.find_one()
        self.connection_mock.find_one.assert_called_once()
        fromPatch.assert_called_once_with(sentinel.find_object)
        self.assertEqual(fighters, sentinel.fighter_object)

    @patch.object(repository, 'fighter_from_document')
    def test_findOneWithArgumentsCallsToCollection(self, fromPatch):
        self.connection_mock.find_one.return_value = sentinel.find_object
        fromPatch.return_value = sentinel.fighter_object
        fighters = self.repository.find_one(something='x', something_else=1)
        self.connection_mock.find_one.assert_called_once(something='x', something_else=1)
        fromPatch.assert_called_once_with(sentinel.find_object)
        self.assertEqual(fighters, sentinel.fighter_object)


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