from provider.db.database import Database
from bson import ObjectId


class UsersRepository:
    def __init__(self, db: Database):
        self.db = db

    def find_one(self, data: dict):
        return self.db.get_users_collection.find_one(data)

    def find_many(self, data: dict):
        return self.db.get_users_collection.find(data)

    def insert_one(self, data: dict) -> ObjectId:
        return self.db.get_users_collection.insert_one(data).inserted_id

    def update_one(self, filter: dict, new_data: dict):
        return self.db.get_users_collection.update_one(filter, new_data)
