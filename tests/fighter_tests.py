import unittest
from tracker import *
from dice import *

class FighterTest(unittest.TestCase):

    def assert_initiative_equals(self, fighter, size, sides, modifier):
        self.assertEqual(fighter.initiative.get_size(), size)
        for d in range(size):
            self.assertEqual(fighter.initiative.get_dice()[d].get_sides(), sides)
        self.assertEqual(fighter.initiative.get_modifier(), modifier)

    def test_initWithNoArgumentHas1d20Initiative(self):
        fighter = Fighter()
        self.assert_initiative_equals(fighter, 1, 20, 0)

    def test_initWith1d20Plus10HasThatForInitiative(self):
        fighter = Fighter(initiative = Pool(dice=[Die(sides=20)], modifier=10))
        self.assert_initiative_equals(fighter, 1, 20, 10)

    def test_initWith2d6HasThatForInitiative(self):
        fighter = Fighter(initiative = Pool(dice=[Die(sides=6) for i in range(2)]))
        self.assert_initiative_equals(fighter, 2, 6, 0)

    def test_initDamakosHasName(self):
        fighter = Fighter(name = "Damakos")
        self.assertEquals(fighter.name, "Damakos")

    def test_initTarkovHasName(self):
        fighter = Fighter(name = "Tarkov")
        self.assertEquals(fighter.name, "Tarkov")

    def test_initWithoutNameHasNoneName(self):
        fighter = Fighter()
        self.assertIsNone(fighter.name)

    def test_initWithoutIdHasNoneId(self):
        fighter = Fighter()
        self.assertIsNone(fighter.id)

    def test_initWithoutIdHasNoneId(self):
        fighter = Fighter()
        self.assertIsNone(fighter.id)

    def test_initId1HasId(self):
        fighter = Fighter(id = 1)
        self.assertEqual(fighter.id, 1)
