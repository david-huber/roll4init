from dice.dice_parser import DiceParser
from tracker.fighter import Fighter

__all__ = ['FighterRepository', 'fighter_from_document', 'fighter_to_document']


def fighter_from_document(doc):
    if doc is None:
        return None
    diceParser = DiceParser();
    return Fighter(id=doc.get("_id"), name=doc.get("name"), initiative=diceParser.parse(doc.get("initiative", "1d20")))

def fighter_to_document(fighter):
    doc = {}
    doc["initiative"] = str(fighter.initiative)
    if not fighter.name is None:
        doc["name"] = fighter.name
    if not fighter.id is None:
        doc["_id"] = fighter.id
    return doc

class FighterRepository:


    def __init__(self, collection):
        self.collection = collection

    def save(self, fighter):
        doc = fighter_to_document(fighter)
        self.collection.save(doc)

    def remove(self, fighter):
        doc = fighter_to_document(fighter)
        del doc["initiative"]
        if len(doc) == 0:
            raise ValueError("fighter must be identified by name or id")
        self.collection.remove(doc)

    def find(self, *args, **kwargs):
        fighterCursor = self.collection.find(*args, **kwargs)
        return list(map(lambda d: fighter_from_document(d), fighterCursor))

    def find_one(self, *args, **kwargs):
        return fighter_from_document(self.collection.find_one(*args, **kwargs))