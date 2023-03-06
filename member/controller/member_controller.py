from abc import ABCMeta

from fastapi import Depends

from member.dto.member_create_dto import MemberCreateDto
from member.dto.member_get_dto import MemberGetDto
from member.dto.user_update_dto import MemberUpdateDto
from member.service.member_service import MemberService
from security.config.jwt_util import get_current_member
from security.dto.jwt import Jwt
from security.dto.login_dto import LoginDto


class MemberController(metaclass=ABCMeta):
    def __init__(self, member_service: MemberService):
        self.member_service = member_service

    def login(self, login_dto: LoginDto) -> Jwt:
        return self.member_service.login(login_dto)

    def create(self, member_create_dto: MemberCreateDto) -> MemberGetDto:
        return self.member_service.create(member_create_dto)

    def delete(self, login_id: str = Depends(get_current_member)):
        self.member_service.delete(login_id)

    def update(
        self,
        user_update_dto: MemberUpdateDto,
        login_id: str = Depends(get_current_member),
    ) -> Jwt:
        return self.member_service.update(login_id, user_update_dto)

    def find_me(self, login_id: str = Depends(get_current_member)) -> MemberGetDto:
        return self.member_service.find_me(login_id)
