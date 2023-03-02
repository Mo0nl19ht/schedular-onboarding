from abc import ABCMeta
from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from starlette import status

from member.domain.member import Member
from member.dto.member_create_dto import MemberCreateDto
from member.dto.member_get_dto import MemberGetDto
from member.dto.user_update_dto import MemberUpdateDto
from member.repository.member_repository import MemberRepository
from security.config.jwt_config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
    TOKEN_TYPE,
)
from security.dto.login_dto import LoginDto
from security.dto.token import Token


class MemberService(metaclass=ABCMeta):
    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def login(self, login_dto: LoginDto):
        member = self.member_repository.find_by_login_id(login_dto.login_id)
        if not member or not member.verify_password(login_dto.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="존재하지 않는 id 또는 password 입니다",
                # headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.make_access_token(member.login_id)
        s = Token(
            access_token=access_token,
            token_type=TOKEN_TYPE,
            login_id=member.login_id,
            type=member.type,
        )
        return s

    def make_access_token(self, login_id: str):
        data = {
            "sub": login_id,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    def create(self, member_create_dto: MemberCreateDto) -> MemberGetDto:
        self._validate_email(member_create_dto.email)
        self._validate_login_id(member_create_dto.login_id)
        member = Member.from_create_dto(member_create_dto)
        return MemberGetDto.from_orm(self.member_repository.create(member))

    def delete(self, login_id: str):
        self.member_repository.delete(login_id)

    def find_by_id(self, member_id: int) -> MemberGetDto:
        return MemberGetDto.from_orm(self.member_repository.find_by_id(member_id))

    def find_by_login_id(self, login_id: str) -> MemberGetDto:
        return MemberGetDto.from_orm(self.member_repository.find_by_login_id(login_id))

    def _validate_email(self, email: str):
        if self.member_repository.find_by_email(email):
            raise HTTPException(status_code=409, detail="이미 존재하는 email 입니다")

    def _validate_login_id(self, login_id: str):
        if self.member_repository.find_by_login_id(login_id):
            raise HTTPException(status_code=409, detail="이미 존재하는 id 입니다")

    def update(self, login_id: str, member_update_dto: MemberUpdateDto):
        member = self.member_repository.find_by_login_id(login_id)
        if not member:
            raise HTTPException(status_code=401, detail="등록된 사용자가 아닙니다")
        if member.login_id != member_update_dto.login_id:
            self._validate_login_id(member_update_dto.login_id)
        if member.email != member_update_dto.email:
            self._validate_email(member_update_dto.email)
        member.update(member_update_dto)
        self.member_repository.update()
