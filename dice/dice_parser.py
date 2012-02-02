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
        
        match = re.match(r"(\d*)d(\d+)([\+\-]\d+)?\s*(?:\(([\+\-]?\d+)\))?", diceString.strip())

        if not match: raiseValueError()

        dice, sides, modifier, showing = match.groups()

        sides = int(sides)

        if not dice: dice = 1
        else: dice = int(dice)

        if not modifier: modifier = 0
        else: modifier = int(modifier)


        if showing:
            showing = int(showing)

            if showing > sides * dice + modifier:
                raiseValueError()

            if showing < dice + modifier:
                raiseValueError()

            if sides > 1:
                numberAtMax = (showing - modifier - dice) / (sides - 1)
                remainder = (showing - modifier) - (numberAtMax * sides) - (dice - numberAtMax - 1)

                def getShowing(index):
                    if index < numberAtMax:
                        return sides
                    if index == numberAtMax:
                        return remainder
                    return 1

                return Pool([Die(sides=int(sides),
                    showing=getShowing(index)) for index in range(dice)], modifier=modifier, rolled=True)


        return Pool([Die(sides=int(sides)) for d in range(dice)], modifier=modifier)







