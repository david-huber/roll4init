import unittest
from dice import *
from mock import patch
import random

class PoolTest(unittest.TestCase):

    def test_sizeEqualsZeroWithZeroDice(self):
        pool = Pool()
        self.assertEqual(pool.get_size(), 0)

    def test_sizeEqualsFourWithFourDice(self):
        dice = [Die() for i in range(4)]
        pool = Pool(dice=dice)
        self.assertEqual(pool.get_size(), 4)

    def test_notRolledWithFourDice(self):
        dice = [Die() for i in range(4)]
        pool = Pool(dice=dice)
        self.assertFalse(pool.is_rolled())

    def test_rolledWithFourDice(self):
        dice = [Die() for i in range(4)]
        pool = Pool(dice=dice, rolled=True)
        self.assertTrue(pool.is_rolled())

    def test_poolWithFourDiceIsRolled(self):
        dice = [Die() for i in range(4)]
        pool = Pool(dice=dice, rolled=False)
        pool.roll()
        self.assertTrue(pool.is_rolled())

    def test_getDiceGetsDiceInPool(self):
        dice = [Die() for i in range(4)]
        pool = Pool(dice=dice)
        self.assertSequenceEqual(pool.get_dice(), dice)

    def test_getModifierWithNoArgsReturns0(self):
        pool = Pool()
        self.assertEqual(pool.get_modifier(), 0)

    def test_getModifierWithNegativeFiveModifierReturnsNegative5(self):
        pool = Pool(modifier=-5)
        self.assertEqual(pool.get_modifier(), -5)

    def test_sumOfSixSnakeEyesIsSix(self):
        dice = [Die() for i in range(6)]
        pool = Pool(dice=dice)
        self.assertEqual(pool.sum(), 6)

    def test_sumOfOneThroughSixIsTwentyOne(self):
        dice = [Die(showing=i+1) for i in range(6)]
        pool = Pool(dice=dice)
        self.assertEqual(pool.sum(), 21)

    def test_sumOfOneThroughSixWithModifierOfFiveIsTwentySix(self):
        dice = [Die(showing=i+1) for i in range(6)]
        pool = Pool(dice=dice, modifier=5)
        self.assertEqual(pool.sum(), 26)

    def test_takeRollsOverFiveForOneThroughSixReturnsASetOf1(self):
        dice = [Die(showing=i+1) for i in range(6)]
        pool = Pool(dice=dice)
        self.assertEqual(pool.take_rolls_over(5).get_size(), 1)

    def test_takeRollsOverTwoForOneThroughSixReturnsASetOf4(self):
        dice = [Die(showing=i+1) for i in range(6)]
        pool = Pool(dice=dice)
        self.assertEqual(pool.take_rolls_over(2).get_size(), 4)

    def test_takeRollsUnderFiveForOneThroughSixReturnsASetOf4(self):
        dice = [Die(showing=i+1) for i in range(6)]
        pool = Pool(dice=dice)
        self.assertEqual(pool.take_rolls_under(5).get_size(), 4)

    def test_takeRollsUnderTwoForOneThroughSixReturnsASetOf1(self):
        dice = [Die(showing=i+1) for i in range(6)]
        pool = Pool(dice=dice)
        self.assertEqual(pool.take_rolls_under(2).get_size(), 1)

    def test_strEmptyPoolIs0d0(self):
        pool = Pool()
        self.assertEqual(str(pool), "0d")

    def test_strRolledEmptyPoolIs0d0(self):
        pool = Pool(rolled=True)
        self.assertEqual(str(pool), "0d")

    def test_strRolledEmptyPoolWithPlus10ModIs0d0plus10(self):
        pool = Pool(rolled=True, modifier=10)
        self.assertEqual(str(pool), "0d+10")

    def test_strOneTwentySidedDieIs1d20(self):
        dice = [Die(sides=20)]
        pool = Pool(dice=dice)
        self.assertEqual(str(pool), "1d20")

    def test_strOneSixSidedDieIs1d6(self):
        dice = [Die(sides=6)]
        pool = Pool(dice=dice)
        self.assertEqual(str(pool), "1d6")

    def test_strOneSixSidedDieRolledAFiveIs1d6noted5(self):
        dice = [Die(sides=6, showing=5)]
        pool = Pool(dice=dice, rolled=True)
        self.assertEqual(str(pool), "1d6 (5)")

    def test_strThreeTenSidedDiceIs3d10(self):
        dice = [Die(sides=10) for i in range(3)]
        pool = Pool(dice=dice)
        self.assertEqual(str(pool), "3d10")

    def test_strThreeTenSidedDiceShowingSevenAndRolledIs3d10noted21(self):
        dice = [Die(sides=10, showing=7) for i in range(3)]
        pool = Pool(dice=dice, rolled=True)
        self.assertEqual(str(pool), "3d10 (21)")

    def test_strThreeTenSidedDicePlusFiveIs3d10plus5(self):
        dice = [Die(sides=10) for i in range(3)]
        pool = Pool(dice=dice, modifier=5)
        self.assertEqual(str(pool), "3d10+5")

    def test_strThreeTenSidedDiceMinusEightIs3d10minus8(self):
        dice = [Die(sides=10) for i in range(3)]
        pool = Pool(dice=dice, modifier=-8)
        self.assertEqual(str(pool), "3d10-8")

    def test_strTwoTwelveSidersPlusThreeFourSidersPlusOneIs2d12plus3d4plus1(self):
        dice = [Die(sides=4), Die(sides=12), Die(sides=12), Die(sides=4), Die(sides=4)]
        pool = Pool(dice=dice, modifier=1)
        self.assertEqual(str(pool), "2d12+3d4+1")

    def test_eqOnTwoNewPoolsReturnsTrue(self):
        self.assertEqual(Pool(), Pool())

    def test_eqOnPoolAndNoneReturnsFalse(self):
        self.assertNotEqual(Pool(), None)

    def test_eqOnPoolAnd1ReturnsFalse(self):
        self.assertNotEqual(Pool(), 1)
        self.assertNotEqual(1, Pool())

    def test_eqOnPoold6AndPoold8ReturnsFalse(self):
        self.assertNotEqual(Pool(dice=[Die(sides=6)]), Pool(dice=[Die(sides=8)]))

    def test_eqOnSimilarRolledPoolsThatSumToSameReturnsTrue(self):
        self.assertEqual(Pool(dice=[Die(sides=6, showing=1), Die(sides=6, showing=6)], rolled=True),
            Pool(dice=[Die(sides=6, showing=4), Die(sides=6, showing=3)], rolled=True))

    def test_eqOnDifferentRolledPoolsThatSumToSameReturnsFalse(self):
        self.assertNotEqual(Pool(dice=[Die(sides=6, showing=1), Die(sides=6, showing=6)], rolled=True),
            Pool(dice=[Die(sides=60, showing=4), Die(sides=60, showing=3)], rolled=True))

    @patch.object(Die, 'roll')
    def test_rollRollsDie(self, dieMock):
        dieMock.return_value = 6
        pool = Pool(dice=[Die()])
        result = pool.roll()
        self.assertTrue(dieMock.called)
        self.assertEqual(result, [6])

    @patch.object(random, 'randint')
    def test_rollDiceWhileUnder5RollsDiceUntilItHasFiveAndSix(self, randintMock):
        randintMock.return_value = 1
        def increment_roll(*args, **kwargs):
            randintMock.return_value += 1
            return randintMock.return_value
        randintMock.side_effect = increment_roll
        pool = Pool(dice=[Die(), Die()])

        result = pool.roll(roll_dice_while=lambda d: d.get_face() < 5)
        self.assertEqual(randintMock.call_count, 5)
        self.assertSequenceEqual(result, [5,6])

    @patch.object(random, 'randint')
    def test_rollDiceUntilOver4RollsDiceUntilItHasFiveAndSix(self, randintMock):
        randintMock.return_value = 1
        def increment_roll(*args, **kwargs):
            randintMock.return_value += 1
            return randintMock.return_value

        randintMock.side_effect = increment_roll
        pool = Pool(dice=[Die(), Die()])

        result = pool.roll(roll_dice_until=lambda d: d.get_face() > 4)
        self.assertEqual(randintMock.call_count, 5)
        self.assertSequenceEqual(result, [5,6])
