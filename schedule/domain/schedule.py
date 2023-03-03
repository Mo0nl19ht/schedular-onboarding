from sqlalchemy import Column, String, Text, DateTime

from common.base_entity import BaseEntity
from schedule.domain.status_enum import Status


class Schedule(BaseEntity):
    __tablename__ = "schedule"

    title = Column(String(255))
    memo = Column(Text)
    status = Column(String(100), default=Status.SCHEDULED.value)
    start = Column(DateTime)
    end = Column(DateTime)

    # @classmethod
    # def from_create_dto(cls, member_create_dto: MemberCreateDto) -> "Member":
    #     return cls(
    #         login_id=member_create_dto.login_id,
    #         name=member_create_dto.name,
    #         email=member_create_dto.email,
    #         hashed_password=cls._hash_password(cls, member_create_dto.password),
    #         type=member_create_dto.type,
    #     )
