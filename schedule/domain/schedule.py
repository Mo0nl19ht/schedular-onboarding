from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from common.base_entity import BaseEntity
from member.domain.user import User
from schedule.domain.status_enum import Status


class Schedule(BaseEntity):
    __tablename__ = "schedule"

    title = Column(String(255), default="schedule title")
    memo = Column(Text, nullable=True)
    status = Column(String(100), default=Status.SCHEDULED.value)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("member.id"), nullable=False)

    user = relationship("User", back_populates="schedules")

    # @classmethod
    # def from_create_dto(cls, member_create_dto: MemberCreateDto) -> "Member":
    #     return cls(
    #         login_id=member_create_dto.login_id,
    #         name=member_create_dto.name,
    #         email=member_create_dto.email,
    #         hashed_password=cls._hash_password(cls, member_create_dto.password),
    #         type=member_create_dto.type,
    #     )
