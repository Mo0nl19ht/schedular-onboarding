from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from member.dto.member_create_dto import MemberCreateDto
from member.dto.user_update_dto import MemberUpdateDto
from member.service.user_service import UserService
from security.dto.login_dto import LoginDto


#
class UserController:
    def __init__(self, user_service: UserService):
        self.router = APIRouter(prefix="/v1/user")
        self.user_service = user_service

        self.router.add_api_route(
            "", self.create, methods=["POST"], status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/{login_id}",
            self.delete,
            methods=["DELETE"],
            status_code=status.HTTP_200_OK,
        )
        self.router.add_api_route(
            "/{login_id}",
            self.update,
            methods=["put"],
            status_code=status.HTTP_200_OK,
        )
        self.router.add_api_route(
            "/{login_id}",
            self.find_by_login_id,
            methods=["get"],
            status_code=status.HTTP_200_OK,
        )
        self.router.add_api_route(
            "/login",
            self.login,
            methods=["post"],
            status_code=status.HTTP_200_OK,
        )

    def login(self, login_dto: LoginDto):
        return self.user_service.login(login_dto)

    def create(self, member_create_dto: MemberCreateDto):
        return self.user_service.create(member_create_dto)

    def delete(self, login_id: str):
        return self.user_service.delete(login_id)

    def update(self, login_id: str, user_update_dto: MemberUpdateDto):
        return self.user_service.update(login_id, user_update_dto)

    def find_by_login_id(self, login_id: str):
        return self.user_service.find_by_login_id(login_id)
