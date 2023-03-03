from common.database import Database

from member.repository.member_repository import MemberRepository


class AdminRepository(MemberRepository):
    def __init__(self, database: Database):
        super().__init__(database)
