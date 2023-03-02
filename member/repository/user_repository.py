from sqlalchemy import select

from common.database import Database
from member.domain.user import User
from member.repository.member_repository import MemberRepository


class UserRepository(MemberRepository):
    def __init__(self, database: Database):
        super().__init__(database)

    def find_by_login_id(self, login_id: str) -> User:
        session = self.get_session()
        query = select(User).filter_by(login_id=login_id)
        return session.scalars(query).first()
