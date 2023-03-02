from passlib.context import CryptContext
from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property

from common.base_entity import BaseEntity
from member.dto.member_create_dto import MemberCreateDto
from member.dto.user_update_dto import MemberUpdateDto


class Member(BaseEntity):
    __tablename__ = "member"
    __table_args__ = {"extend_existing": True}
    # __abstract__ = True

    login_id = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    name = Column(String(255))
    hashed_password = Column(String(255))
    type = Column(String(255))

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "member"}

    @classmethod
    def from_create_dto(cls, member_create_dto: MemberCreateDto) -> "Member":
        return cls(
            login_id=member_create_dto.login_id,
            name=member_create_dto.name,
            email=member_create_dto.email,
            hashed_password=cls._hash_password(member_create_dto.password),
            type=member_create_dto.type,
        )

    def _hash_password(password: str):
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

    def update(self, member_update_dto: MemberUpdateDto):
        self.login_id = member_update_dto.login_id
        self.email = member_update_dto.email
        self.name = member_update_dto.name
