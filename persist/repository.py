from dice.dice_parser import DiceParser
from tracker.fighter import Fighter

__all__ = ['FighterRepository', 'fighter_from_document']


def fighter_from_document(doc):
    if doc is None:
        return None
    diceParser = DiceParser();
    return Fighter(id=doc.get("_id"), name=doc.get("name"), initiative=diceParser.parse(doc.get("initiative", "1d20")))

class FighterRepository:
    
    def __init__(self, collection):
        self.collection = collection

    def _fighter_to_doc(self, fighter):
        doc = {}
        doc["initiative"] = str(fighter.initiative)
        if not fighter.name is None:
            doc["name"] = fighter.name
        if not fighter.id is None:
            doc["_id"] = fighter.id
        return doc

    def save(self, fighter):
        doc = self._fighter_to_doc(fighter)
        self.collection.save(doc)

    def remove(self, fighter):
        doc = self._fighter_to_doc(fighter)
        del doc["initiative"]
        if len(doc) == 0:
            raise ValueError("fighter must be identified by name or id")
        self.collection.remove(doc)

