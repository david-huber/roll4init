import random

__all__ = ['Die']

class Die:

    def __init__(self, sides=6, showing=1):
        if sides <= 0:
            raise ValueError("A Die must have 0 or more sides")
        if showing <= 0:
            raise ValueError("A Die cannot show less than 0")
        if showing > sides:
            raise ValueError("A Die cannot show greater than its sides")
        self._sides = sides
        self._face = showing

    def get_face(self):
        return self._face

    def get_sides(self):
        return self._sides

    def roll(self, roll_while=None, roll_until=None):
        if roll_while != None and roll_until != None:
            raise ValueError("roll_while cannot be used in conjunction with roll_until")

        if roll_while != None:
            roll_predicate = lambda d: roll_while(d)
        elif roll_until != None:
            roll_predicate = lambda d: not roll_until(d)
        else:
            roll_predicate = lambda d: False

        def rollAndCheck():
            self._face = random.randint(1, self._sides)
            return roll_predicate(self)

        while(rollAndCheck()):
            pass

        return self.get_face()