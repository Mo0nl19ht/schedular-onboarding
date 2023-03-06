from typing import List

from fastapi import HTTPException
from starlette import status

from member.domain.user import User
from member.dto.member_get_dto import UserGetDto
from member.dto.user_update_dto import MemberUpdateDto
from member.repository.admin_repository import AdminRepository
from member.service.member_service import MemberService


class AdminService(MemberService):
    def __init__(self, admin_repository: AdminRepository):
        super().__init__(admin_repository)
        self.admin_repository = admin_repository

    def find_all_user(self, login_id: str) -> List[UserGetDto]:
        self._get_current_admin(login_id)
        users = self.admin_repository.find_all_user()

        return self._to_user_get_dtos(users)

    def find_user_by_login_id(self, user_id: str, login_id: str) -> UserGetDto:
        self._get_current_admin(login_id)
        return UserGetDto.from_orm(self.admin_repository.find_by_login_id(user_id))

    def update_user(
        self, user_id: str, member_update_dto: MemberUpdateDto, login_id: str
    ) -> UserGetDto:
        self._is_me(user_id, login_id)
        self._get_current_admin(login_id)
        user = self._get_user(user_id)

        self._validate_for_update(user, member_update_dto)
        user.update(member_update_dto)

        return UserGetDto.from_orm(self.admin_repository.update(user))

    def delete_user(self, user_id: str, login_id: str):
        self._is_me(user_id, login_id)
        self._get_current_admin(login_id)
        user = self._get_user(user_id)
        print(111)
        print(user)
        self.member_repository.delete(user)

    def _get_user(self, user_id):
        user = self.admin_repository.find_by_login_id(user_id)
        self._validate_user(user)
        return user

    def _validate_user(self, user):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 user입니다"
            )
        if user.type != "user":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="관리자는 user의 정보만 변경 가능합니다"
            )

    def _get_current_admin(self, login_id):
        admin = self.admin_repository.find_by_login_id(login_id)
        self._validate_admin(admin)
        return admin

    def _validate_admin(self, admin):
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="등록된 사용자가 아닙니다"
            )
        if admin.type != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="admin만 가능한 작업입니다"
            )

    def _to_user_get_dtos(self, users: List[User]) -> List[UserGetDto]:
        dtos = []
        for user in users:
            dtos.append(UserGetDto.from_orm(user))
        return dtos

    def _is_me(self, user_id, login_id):
        if user_id == login_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="본인 계정은 관리할 수 없습니다, 직접 변경하세요",
            )
