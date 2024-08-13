from fastapi import APIRouter
from provider.auth.auth_service import AuthService
from provider.core.users_service import UsersService
from provider.schemas.refresh_schema import RefreshToken
from provider.schemas.user_schema import UseCreationDTO
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

class AuthRouter:
    def __init__(self, users_service: UsersService, auth_service: AuthService):
        self.router = APIRouter(prefix="/api/v1", tags=["auth"])
        self.auth_service = auth_service
        self.users_service = users_service

    def get_routers(self) -> APIRouter:
        self.router.post("/signup")(self.signup)
        self.router.post("/signin")(self.signin)
        self.router.post("/refresh")(self.refresh)
        return self.router

    def signup(self, user_data: UseCreationDTO) -> dict:
        return {"data": {"user_id": self.users_service.create_user(user_data.model_dump())}}

    def signin(self, form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
        return {
            "data": {
                "access_token": self.auth_service.create_access_token(id, role),
                "refresh_token": self.auth_service.create_refresh_token(id),
                "token_type": "bearer",
            }
        }

    def refresh(self, refresh_token: RefreshToken) -> dict:
        return {
            "data": {
                "access_token": self.auth_service.create_access_token(id, role),
                "refresh_token": self.auth_service.create_refresh_token(id),
                "token_type": "bearer",
            }
        }
