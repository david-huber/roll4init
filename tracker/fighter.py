from dice import *

__all__ = ['Fighter']

class Fighter:

    def __init__(self, initiative=Pool(dice=[Die(sides=20)])):
        self.initiative = initiative
