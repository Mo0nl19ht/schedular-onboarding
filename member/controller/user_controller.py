from fastapi import APIRouter, Depends

from member.dto.member_create_dto import MemberCreateDto
from member.dto.member_get_dto import MemberGetDto
from member.dto.user_update_dto import MemberUpdateDto
from member.service.user_service import UserService
from security.config.jwt_util import get_current_member
from security.dto.jwt import Jwt
from security.dto.login_dto import LoginDto


class UserController:
    def __init__(self, user_service: UserService):
        self.router = APIRouter(prefix="/v1/user")
        self.user_service = user_service

        self.router.add_api_route("", self.create, methods=["POST"])
        self.router.add_api_route("", self.delete, methods=["DELETE"])
        self.router.add_api_route("", self.update, methods=["put"])
        self.router.add_api_route("", self.find_by_login_id, methods=["get"])
        self.router.add_api_route("/login", self.login, methods=["post"])

    def login(self, login_dto: LoginDto) -> Jwt:
        return self.user_service.login(login_dto)

    def create(self, member_create_dto: MemberCreateDto) -> MemberGetDto:
        return self.user_service.create(member_create_dto)

    def delete(self, login_id: str = Depends(get_current_member)):
        return self.user_service.delete(login_id)

    def update(
        self,
        user_update_dto: MemberUpdateDto,
        login_id: str = Depends(get_current_member),
    ) -> Jwt:
        return self.user_service.update(login_id, user_update_dto)

    def find_by_login_id(
        self, login_id: str = Depends(get_current_member)
    ) -> MemberGetDto:
        return self.user_service.find_by_login_id(login_id)
