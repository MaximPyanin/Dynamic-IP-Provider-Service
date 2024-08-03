from datetime import datetime, timedelta
import uuid
from uuid import UUID
from bson import ObjectId
from provider.constants.exceptions import Exceptions
from provider.constants.roles import Roles
from provider.db.repositories.users_repository import UsersRepository
from provider.utils.jwt_service import JWTService
from provider.utils.hash_service import HashService


class AuthService:
    def __init__(self, users_repository: UsersRepository, jwt_service: JWTService):
        self.jwt_service = jwt_service
        self.users_repository = users_repository

    def authenticate_user(self, email: str, password: str) -> tuple:
        try:
            user = self.users_repository.find_one({"email": email})
        except Exception:  # concr
            raise Exceptions.AUTHENTICATION_ERROR.value
        if not HashService.check_password(password, user["password"].encode()):
            raise Exceptions.AUTHENTICATION_ERROR.value
        return user["_id"], user["role"]

    def create_access_token(self, id: ObjectId, role: Roles) -> str | bytes:
        return self.jwt_service.encode_jwt(
            {"id": id.binary.encode(), "role": role.value}
        )

    def decode_jwt(self, token: str | bytes) -> dict:
        return self.jwt_service.decode_jwt(token)

    def create_refresh_token(self, id: ObjectId, expire_days: int = 30) -> UUID:
        refresh_token = uuid.uuid4()
        self.users_repository.update_one(
            {"_id": id},
            {
                "refresh_token": refresh_token,
                "expired_at": datetime.utcnow() + timedelta(days=expire_days),
            },
        )
        return refresh_token

    def get_by_refresh_token(self, token: UUID) -> (ObjectId, Roles):
        try:
            user = self.users_repository.find_one({"refresh_token": token})
        except Exception:  #
            raise Exceptions.AUTHENTICATION_ERROR.value
        if user["expired_at"] <= datetime.utcnow():
            raise Exceptions.AUTHENTICATION_ERROR.value
        return user["_id"], user["role"]
