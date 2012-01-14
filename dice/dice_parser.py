from dice import Die
from pool import Pool
import re

__all__ = ['DiceParser']

class DiceParser:

    def __init__(self):
        pass

    def parse(self, diceString):
        def raiseValueError():
            raise ValueError("Invalid diceString value: {0}".format(diceString))

        if not diceString: raiseValueError()
        
        match = re.match(r"(\d*)d(\d+)([\+\-]\d+)?", diceString.strip())

        if not match: raiseValueError()

        dice, sides, modifier = match.groups()

        if not dice: dice = 1

        if not modifier: modifier = 0

        return Pool([Die(sides=int(sides)) for d in range(int(dice))], modifier=int(modifier))