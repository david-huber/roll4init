__all__ = ['FighterRepository']

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

    def find_one(self, spec=None):
        return self.collection.find_one(spec=spec)