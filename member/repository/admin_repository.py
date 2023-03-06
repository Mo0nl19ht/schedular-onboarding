from typing import List

from sqlalchemy import select

from common.database import Database
from member.domain.member import Member
from member.domain.user import User

from member.repository.member_repository import MemberRepository


class AdminRepository(MemberRepository):
    def __init__(self, database: Database):
        super().__init__(database)

    def find_all_user(self) -> List[User]:
        session = self.get_session()
        query = select(User)
        return session.scalars(query).all()
