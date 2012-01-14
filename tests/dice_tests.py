import unittest
from dice import *
from mock import patch
import random

class DieTest(unittest.TestCase):

    def test_negativeOneSidesThrowsValueException(self):
        self.assertRaises(ValueError, Die, (-1))

    def test_zeroSidesThrowsValueException(self):
        self.assertRaises(ValueError, Die, (0))

    def test_noArgumentsShowing1(self):
        self.assertEqual(Die().get_face(), 1)

    def test_noArgumentsHasSixSides(self):
        self.assertEqual(Die().get_sides(), 6)

    def test_withSevenSidesHasSevenSides(self):
        self.assertEqual(Die(7).get_sides(), 7)

    def test_sevenSidedDiceShows1(self):
        self.assertEqual(Die(sides=7).get_face(), 1)

    def test_showing6Shows6(self):
        self.assertEqual(Die(showing=6).get_face(), 6)

    def test_showingMoreThanSidesThrowsValueException(self):
        self.assertRaises(ValueError, Die, showing=8, sides=7)

    def test_showingZeroThrowsValueException(self):
        self.assertRaises(ValueError, Die, showing=0)

    def test_showingNegativeOneThrowsValueException(self):
        self.assertRaises(ValueError, Die, showing=-1)

    @patch.object(random, 'randint')
    def test_rollCallsRandomInt(self, randintMock):
        die = Die(sides=1337)
        die.roll()
        randintMock.assert_called_once_with(1, 1337)

    @patch.object(random, 'randint')
    def test_rollReturnsRandomInt(self, randintMock):
        randintMock.return_value = 123
        die = Die(sides=1337)
        result = die.roll()
        self.assertEquals(result, 123)

    @patch.object(random, 'randint')
    def test_rollShowsRandomInt(self, randintMock):
        randintMock.return_value = 123
        die = Die(sides=1337)
        die.roll()
        self.assertEquals(die.get_face(), 123)

    @patch.object(random, 'randint')
    def test_rollWhileLessThan3KeepsRollingTilResultIsThree(self, randintMock):
        randintMock.return_value = 0
        def increment_roll(*args, **kwargs):
            randintMock.return_value += 1
            return randintMock.return_value 
        randintMock.side_effect = increment_roll
        die = Die()
        result = die.roll(roll_while=lambda d: d.get_face() < 3)
        self.assertEqual(result, 3)
        self.assertEqual(randintMock.call_count, 3)

    @patch.object(random, 'randint')
    def test_rollUntilGreaterThan5KeepsRollingTilResultIsSix(self, randintMock):
        randintMock.return_value = 0
        def increment_roll(*args, **kwargs):
            randintMock.return_value += 1
            return randintMock.return_value
        randintMock.side_effect = increment_roll
        die = Die()
        result = die.roll(roll_until=lambda d: d.get_face() > 5)
        self.assertEqual(result, 6)
        self.assertEqual(randintMock.call_count, 6)

    def test_rollWithWhileAndTilThrowsValueError(self):
        die = Die()
        self.assertRaises(ValueError, die.roll, roll_while=lambda d: False, roll_until=lambda d: True)