from fastapi import APIRouter, Depends
from starlette import status

from member.controller.member_controller import MemberController
from member.service.user_service import UserService


class UserController(MemberController):
    def __init__(self, user_service: UserService):
        super().__init__(user_service)
        self.router = APIRouter(prefix="/v1/user")
        self.user_service = user_service

        self.router.add_api_route("", self.create, methods=["POST"])
        self.router.add_api_route(
            "", self.delete, methods=["DELETE"], status_code=status.HTTP_202_ACCEPTED
        )
        self.router.add_api_route("", self.update, methods=["put"])
        self.router.add_api_route("", self.find_me, methods=["get"])
        self.router.add_api_route("/login", self.login, methods=["post"])

    # def login(self, login_dto: LoginDto) -> Jwt:
    #     return self.user_service.login(login_dto)
    #
    # def create(self, member_create_dto: MemberCreateDto) -> MemberGetDto:
    #     return self.user_service.create(member_create_dto)
    #
    # def delete(self, login_id: str = Depends(get_current_member)):
    #     self.user_service.delete(login_id)
    #
    # def update(
    #     self,
    #     user_update_dto: MemberUpdateDto,
    #     login_id: str = Depends(get_current_member),
    # ) -> Jwt:
    #     return self.user_service.update(login_id, user_update_dto)
    #
    # def find_me(self, login_id: str = Depends(get_current_member)) -> MemberGetDto:
    #     return self.user_service.find_me(login_id)
