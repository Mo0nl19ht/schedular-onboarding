from datetime import datetime


from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from common.base_entity import BaseEntity
from schedule.common.config import DATE_FORMAT

from schedule.enum.status import Status
from schedule.dto.schedule_dto import ScheduleCreateDto, ScheduleUpdateCreateDto


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
        cls, schedule_dto: ScheduleCreateDto, user_id: str
    ) -> "Schedule":
        schedule = cls(
            title=schedule_dto.title,
            memo=schedule_dto.memo,
            start=cls._transfrom_to_datetime(cls, schedule_dto.start),
            end=cls._transfrom_to_datetime(cls, schedule_dto.end),
            user_id=user_id,
        )

        schedule._set_status()
        return schedule

    def update(self, schedule_update_dto: ScheduleUpdateCreateDto):
        self.title = schedule_update_dto.title
        self.memo = schedule_update_dto.memo
        self.start = self._transfrom_to_datetime(schedule_update_dto.start)
        self.end = self._transfrom_to_datetime(schedule_update_dto.end)
        self._set_status()

    def _set_status(self):
        if self.start > datetime.now():
            self.status = Status.SCHEDULED.value
        elif self.start <= datetime.now() <= self.end:
            self.status = Status.IN_PROGRESS.value
        else:
            self.status = Status.COMPLETED.value

    def _transfrom_to_datetime(self, str_date: str):
        return datetime.strptime(str_date, DATE_FORMAT)
