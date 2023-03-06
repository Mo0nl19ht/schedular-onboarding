from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from member.controller.member_controller import MemberController
from member.dto.member_get_dto import UserGetDto
from member.dto.user_update_dto import MemberUpdateDto
from member.service.admin_service import AdminService
from security.config.jwt_util import get_current_member


class AdminController(MemberController):
    def __init__(self, admin_service: AdminService):
        super().__init__(admin_service)
        self.router = APIRouter(prefix="/v1/admin")
        self.admin_service = admin_service

        self.router.add_api_route("", self.create, methods=["POST"])
        self.router.add_api_route(
            "", self.delete, methods=["DELETE"], status_code=status.HTTP_202_ACCEPTED
        )
        self.router.add_api_route("", self.update, methods=["put"])
        self.router.add_api_route("", self.find_me, methods=["get"])
        self.router.add_api_route("/login", self.login, methods=["post"])

        # user 관리 api
        self.router.add_api_route("/users", self.find_all_user, methods=["get"])
        self.router.add_api_route(
            "/users/{user_id}", self.find_user_by_login_id, methods=["get"]
        )
        self.router.add_api_route("/users/{user_id}", self.update_user, methods=["put"])
        self.router.add_api_route(
            "/users/{user_id}",
            self.delete_user,
            methods=["DELETE"],
            status_code=status.HTTP_202_ACCEPTED,
        )

    def find_all_user(
        self, login_id: str = Depends(get_current_member)
    ) -> List[UserGetDto]:
        return self.admin_service.find_all_user(login_id)

    def find_user_by_login_id(
        self, user_id: str, login_id: str = Depends(get_current_member)
    ) -> UserGetDto:
        return self.admin_service.find_user_by_login_id(user_id, login_id)

    def update_user(
        self,
        user_id: str,
        member_update_dto: MemberUpdateDto,
        login_id: str = Depends(get_current_member),
    ) -> UserGetDto:
        return self.admin_service.update_user(user_id, member_update_dto, login_id)

    def delete_user(self, user_id: str, login_id: str = Depends(get_current_member)):
        self.admin_service.delete_user(user_id, login_id)
