from fastapi import APIRouter
from provider.schemas.user_schema import UseCreationDTO


class AuthRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/api/v1", tags=["auth"])

    def get_routers(self) -> APIRouter:
        return self.router

    async def signup(self, user_data: UseCreationDTO):
        pass
