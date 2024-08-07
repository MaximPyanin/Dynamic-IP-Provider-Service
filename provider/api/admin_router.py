from typing import Any, Mapping

from fastapi import APIRouter
from pymongo.command_cursor import CommandCursor

from provider.auth.auth_service import AuthService
from provider.core.admin_service import AdminService
from bson import ObjectId

from provider.schemas.user_schema import UserUpdateDTO
from fastapi import Depends


class AdminRouter:
    def __init__(self, admin_service: AdminService, auth_service: AuthService):
        self.admin_service = admin_service
        self.auth_service = auth_service
        self.router = APIRouter(
            prefix="/api/v1/admin",
            tags=["admin"],
            dependencies=[Depends(self.auth_service.validate_user)],
        )

    def get_router(self) -> APIRouter:
        self.router.delete("/{user_id}")(self.remove_user)
        self.router.get("/{user_id}")(self.get_user_info)
        self.router.put("/{user_id}")(self.modify_account_type)
        self.router.get("/", response_model=None)(self.get_all_users)
        return self.router

    def get_user_info(self, user_id: ObjectId) -> dict:
        user_info, user_bindings = self.admin_service.get_user_info(user_id)
        return {
            "user_info": user_info,
            "current_binding": user_bindings[0],
            "bindings_history": user_bindings,
        }

    def get_all_users(
        self, sort: str | None = None, limit: int | None = 20, skip: int | None = 0
    ) -> CommandCursor[Mapping[str, Any] | Any]:
        return self.admin_service.get_all_users(sort, limit, skip)

    def modify_account_type(
        self, user_id: ObjectId, new_type: UserUpdateDTO
    ) -> Mapping[str, Any]:
        return self.admin_service.update_account_type(user_id, new_type.model_dump())

    def remove_user(self, user_id: ObjectId) -> Mapping[str, Any]:
        return self.admin_service.delete_user(user_id)
