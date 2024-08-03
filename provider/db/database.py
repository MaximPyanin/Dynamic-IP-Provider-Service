from typing import Mapping, Any

from pymongo import MongoClient
from pymongo.collection import Collection
from provider.services.config_service import AppConfig


class Database:
    def __init__(self, config: AppConfig):
        self._client = MongoClient(config.MONGO_URI)
        self.db = self._client.get_database("ip-provider")
        self.users_collection = self.db.get_collection("users_collection")
        self.addresses_collection = self.db.get_collection("addresses_collection")

    @property
    def get_users_collection(self) -> Collection[[Mapping[str, Any]]]:
        return self.users_collection

    @property
    def get_addresses_collection(self) -> Collection[[Mapping[str, Any]]]:
        return self.addresses_collection
