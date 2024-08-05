from typing import Any, Mapping

from fastapi import APIRouter

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
        self.router.put("/{user_id}")(self.modify_account_type)
        return self.router

    def modify_account_type(
        self, user_id: ObjectId, new_type: UserUpdateDTO
    ) -> Mapping[str, Any]:  #
        return self.admin_service.update_account_type(user_id, new_type.model_dump())

    def remove_user(self, user_id: ObjectId) -> Mapping[str, Any]:
        return self.admin_service.delete_user(user_id)
        # 5 for premium and change it updated at created at
