from itertools import groupby

__all__ = ['Pool']

class Pool:

    def __init__(self, dice=[], modifier=0):
        self._dice = tuple(d for d in dice)
        self._modifier = modifier

    def get_size(self):
        return len(self._dice)

    def get_dice(self):
        return self._dice

    def get_modifier(self):
        return self._modifier

    def roll(self, roll_dice_while=None, roll_dice_until=None):
        return map(lambda d: d.roll(roll_while=roll_dice_while, roll_until=roll_dice_until), self._dice)

    def sum(self):
        return sum(die.get_face() for die in self._dice) + self._modifier

    def take_rolls_over(self, limit):
        return self._filter_rolls(lambda d: d.get_face() > limit)

    def take_rolls_under(self, limit):
        return self._filter_rolls(lambda d: d.get_face() < limit)

    def _filter_rolls(self, function):
        return Pool(filter(function, self._dice))

    def __str__(self):
        diceStrings = ["d{0}".format(d.get_sides()) for d in sorted(self._dice, key=lambda d: d.get_sides(), reverse=True)]
        summedStrings = ["{0}{1}".format(len(list(group)), key) for key, group in groupby(diceStrings)]
        diceStr = "+".join(summedStrings)

        if self._modifier > 0:
            diceStr += '+{0}'.format(self._modifier)
        elif self._modifier < 0:
            diceStr += str(self._modifier)

        return diceStr