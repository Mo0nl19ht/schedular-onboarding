from member.repository.user_repository import UserRepository
from member.service.member_service import MemberService


class UserService(MemberService):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
