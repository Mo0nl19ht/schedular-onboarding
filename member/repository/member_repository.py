from sqlalchemy import select

from common.repository import Repository
from member.domain.member import Member


class MemberRepository(Repository):
    def create(self, member: Member) -> Member:
        session = self.get_session()
        session.add(member)
        session.commit()
        session.refresh(member)
        return member

    def find_by_id(self, member_id: int) -> Member:
        session = self.get_session()
        query = select(Member).filter_by(id=member_id)
        return session.scalars(query).first()

    def find_by_login_id(self, login_id: str) -> Member:
        session = self.get_session()
        query = select(Member).filter_by(login_id=login_id)
        return session.scalars(query).first()

    def find_by_email(self, email: str) -> Member:
        session = self.get_session()
        query = select(Member).filter_by(email=email)
        return session.scalars(query).first()

    def delete(self, login_id: int):
        member = self.find_by_login_id(login_id)
        if member:
            session = self.get_session()
            session.delete(member)
            session.commit()

    def update(self):
        session = self.get_session()
        session.commit()
