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

    def test_parse2d6noting7ReturnsRolledPoolSummedTo7(self):
        parser = DiceParser()
        pool = parser.parse("2d6 (7)")
        self.assertTrue(pool.is_rolled())
        self.assertEqual(pool.sum(), 7)

    def test_parse1d10minus10notingNegativeFiveReturnsRolledPoolSummedToNegative5(self):
        parser = DiceParser()
        pool = parser.parse("1d10-10 (-5)")
        self.assertTrue(pool.is_rolled())
        self.assertEqual(pool.sum(), -5)


    def test_parse2d12plus5noting20ReturnsRolledPoolSummedTo20(self):
        parser = DiceParser()
        pool = parser.parse("2d12+5 (20)")
        self.assertTrue(pool.is_rolled())
        self.assertEqual(pool.sum(), 20)

    def test_parse2d12minus10noting2ReturnsRolledPoolSummedTo2(self):
        parser = DiceParser()
        pool = parser.parse("2d12-10 (2)")
        self.assertTrue(pool.is_rolled())
        self.assertEqual(pool.sum(), 2)

    def test_parse11d17minus3noting41ReturnsRolledPoolSummedTo41(self):
        parser = DiceParser()
        pool = parser.parse("11d17-3 (41)")
        self.assertTrue(pool.is_rolled())
        self.assertEqual(pool.sum(), 41)


    def test_parse7d3plus50noting60ReturnsRolledPoolSummedTo60(self):
        parser = DiceParser()
        pool = parser.parse("7d3+50 (60)")
        self.assertTrue(pool.is_rolled())
        self.assertEqual(pool.sum(), 60)

    def test_parse2d100minus99noting101ReturnsRolledPoolSummedTo101(self):
        parser = DiceParser()
        pool = parser.parse("2d100-99 (101)")
        self.assertTrue(pool.is_rolled())
        self.assertEqual(pool.sum(), 101)

    def test_parseImpossiblyHighRollThrowsValueError(self):
        parser = DiceParser()
        self.assertRaises(ValueError, parser.parse, "1d6 (7)")
        self.assertRaises(ValueError, parser.parse, "2d10-1 (20)")
        self.assertRaises(ValueError, parser.parse, "3d7-10 (1000)")

    def test_parseImpossiblyLowRollThrowsValueError(self):
        parser = DiceParser()
        self.assertRaises(ValueError, parser.parse, "1d6 (0)")
        self.assertRaises(ValueError, parser.parse, "2d10-1 (-10)")
        self.assertRaises(ValueError, parser.parse, "3d7-10 (-40)")