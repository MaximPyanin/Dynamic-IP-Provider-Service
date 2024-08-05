from typing import Any, Mapping

from fastapi import APIRouter

from provider.auth.auth_service import AuthService
from provider.schemas.binding_schema import BindingCreationDTO, BindingUpdateDTO

from bson import ObjectId

from provider.core.users_service import UsersService

from fastapi import Depends


class UsersRouter:
    def __init__(self, users_service: UsersService, auth_service: AuthService):
        self.users_service = users_service
        self.auth_service = auth_service
        self.router = APIRouter(
            prefix="/api/v1/users",
            tags=["users"],
            dependencies=[Depends(self.auth_service.validate_user)],
        )

    def get_router(self) -> APIRouter:
        self.router.get("/bindings/count/{user_id}")(self.get_open_bindings_count)
        self.router.post("/bindings")(self.create_binding)
        self.router.get("/bindings/{user_id}")(self.get_user_bindings)
        self.router.delete("/bindings/{binding_id}")(self.remove_binding)
        self.router.put("/bindings/{binding_id}")(self.modify_binding)
        return self.router

    def get_open_bindings_count(self, user_id: ObjectId) -> dict:
        return {"count": self.users_service.get_open_bindings_count(user_id)}

    def create_binding(self, binding: BindingCreationDTO) -> dict:
        return {"binding_id": self.users_service.create_binding(binding.dict())}

    def get_user_bindings(self, user_id: ObjectId) -> dict:
        current_binding, bindings_history = self.users_service.get_bindings(user_id)
        return {
            "current_binding": current_binding,
            "bindings_history": bindings_history,
        }

    def remove_binding(self, binding_id: ObjectId) -> dict:
        return {"deleted_count": self.users_service.delete_binding(binding_id)}

    def modify_binding(
        self, binding_id: ObjectId, new_binding: BindingUpdateDTO
    ) -> Mapping[str, Any]:  #
        return self.users_service.update_binding(binding_id, new_binding.model_dump())
