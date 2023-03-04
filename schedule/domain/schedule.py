from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from starlette import status

from common.base_entity import BaseEntity
from member.domain.user import User
from schedule.domain.status_enum import Status
from schedule.dto.schedule_create_dto import ScheduleCreateDto


class Schedule(BaseEntity):
    __tablename__ = "schedule"

    title = Column(String(255), default="schedule title")
    memo = Column(Text, nullable=True)
    status = Column(String(100), default=Status.SCHEDULED.value)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("member.id"), nullable=False)

    user = relationship("User", back_populates="schedules")

    @classmethod
    def from_create_dto(
        cls, schedule_create_dto: ScheduleCreateDto, user_id: str
    ) -> "Schedule":
        schedule = cls(
            title=schedule_create_dto.title,
            memo=schedule_create_dto.memo,
            start=cls._transfrom_to_datetime(cls, schedule_create_dto.start),
            end=cls._transfrom_to_datetime(cls, schedule_create_dto.end),
            user_id=user_id,
        )

        schedule._set_status()
        return schedule

    def _set_status(self) -> str:
        if self.start > datetime.now():
            self.status = Status.SCHEDULED.value
        elif self.start <= datetime.now() <= self.end:
            self.status = Status.IN_PROGRESS.value
        else:
            self.status = Status.COMPLETED.value

    def _transfrom_to_datetime(self, str_date: str):
        # yyyy-mm-dd-hh:mm
        date_format = "%Y-%m-%d-%H:%M"
        try:
            return datetime.strptime(str_date, date_format)
        except:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 시간 형식입니다",
            )
