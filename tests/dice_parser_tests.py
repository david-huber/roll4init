import unittest
from dice import *

class DiceParserTest(unittest.TestCase):

    def test_parseNoneRaisesValueException(self):
        parser = DiceParser()
        self.assertRaises(ValueError, parser.parse, None)

    def test_parseGarbageRaisesValueException(self):
        parser = DiceParser()
        self.assertRaises(ValueError, parser.parse, "Garbage")

    def test_1plus1RaisesValueException(self):
        parser = DiceParser()
        self.assertRaises(ValueError, parser.parse, "1+1")

    def test_parse1d6ReturnsPoolWithOneSixSidedDie(self):
        parser = DiceParser()
        pool = parser.parse("1d6")
        self.assertEqual(pool.get_size(), 1)
        self.assertEqual(pool.get_dice()[0].get_sides(), 6)

    def test_parse1d6WithWhitespaceReturnsPoolWithOneSixSidedDie(self):
        parser = DiceParser()
        pool = parser.parse(" 1d6 ")
        self.assertEqual(pool.get_size(), 1)
        self.assertEqual(pool.get_dice()[0].get_sides(), 6)

    def test_parsed6ReturnsPoolWithOneSixSidedDie(self):
        parser = DiceParser()
        pool = parser.parse("d6")
        self.assertEqual(pool.get_size(), 1)
        self.assertEqual(pool.get_dice()[0].get_sides(), 6)

    def test_parse2d6ReturnsPoolWithTwoSixSidedDie(self):
        parser = DiceParser()
        pool = parser.parse("2d6")
        self.assertEqual(pool.get_size(), 2)
        self.assertEqual(len(filter(lambda d: d.get_sides() == 6, pool.get_dice())), 2)

    def test_parse2d12ReturnsPoolWithTwoTwelveSidedDie(self):
        parser = DiceParser()
        pool = parser.parse("2d12")
        self.assertEqual(pool.get_size(), 2)
        self.assertEqual(len(filter(lambda d: d.get_sides() == 12, pool.get_dice())), 2)

    def test_parse2d6ReturnsPoolWithModifierOfZero(self):
        parser = DiceParser()
        pool = parser.parse("2d6")
        self.assertEqual(pool.get_modifier(), 0)

    def test_parse2d12plus5ReturnsPoolWithModifierOfFive(self):
        parser = DiceParser()
        pool = parser.parse("2d12+5")
        self.assertEqual(pool.get_modifier(), 5)

    def test_parse2d12minus10ReturnsPoolWithModifierOfNegative10(self):
        parser = DiceParser()
        pool = parser.parse("2d12-10")
        self.assertEqual(pool.get_modifier(), -10)