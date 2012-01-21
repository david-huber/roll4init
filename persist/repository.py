__all__ = ['FighterRepository']

class FighterRepository:
    
    def __init__(self, collection):
        self.collection = collection
    
    def save(self, fighter):
        doc = {}
        doc["initiative"] = str(fighter.initiative)
        if not fighter.name is None:
            doc["name"] = fighter.name
        if not fighter.id is None:
            doc["_id"] = fighter.id
        self.collection.save(doc)
