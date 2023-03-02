from member.dto.user_update_dto import MemberUpdateDto
from member.repository.admin_repository import AdminRepository
from member.repository.user_repository import UserRepository
from member.service.member_service import MemberService


class AdminService(MemberService):
    def __init__(self, admin_repository: AdminRepository):
        super().__init__(admin_repository)
