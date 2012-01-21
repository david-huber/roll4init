from dice import *

__all__ = ['Fighter']

class Fighter:

    def __init__(self, id=None, name=None, initiative=Pool(dice=[Die(sides=20)])):
        self.initiative = initiative
        self.name = name
        self.id = id
