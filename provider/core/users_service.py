from provider.db.repositories.users_repository import UsersRepository
from bson import ObjectId
from provider.utils.hash_service import HashService
from provider.constants.exceptions import Exceptions


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def create_user(self, data: dict) -> ObjectId:
        try:
            self.users_repository.find_one({"email": data["email"]})
        except Exception:  # which error roles
            data["password"] = HashService.hash_password(data["password"]).decode()
            data.update({"refresh_token": None, "expired_at": None})
            if data["role"].value == "USER":
                data.update({"is_premium": False, "bindings_left": 1})
            else:
                data.update({"is_premium": None, "bindings_left": None})
            return self.create_user(data)
        else:
            raise Exceptions.EMAIL_ERROR.value

    def notify(self) -> None:
        pass
