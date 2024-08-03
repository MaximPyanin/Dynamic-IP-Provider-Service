from provider.db.database import Database


class AddressesRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_one(self, data: dict):
        return self.db.get_addresses_collection.find_one(data)

    def find_many(self, data: dict):
        return self.db.get_addresses_collection.find(data)
