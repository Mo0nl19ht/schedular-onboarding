from datetime import datetime

from pydantic import BaseModel

from schedule.domain.schedule import Schedule


class ScheduleGetDto(BaseModel):
    id: int
    title: str
    memo: str
    start: datetime
    end: datetime
    login_id: str

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, schedule: Schedule, login_id: str) -> "ScheduleGetDto":
        return cls(
            id=schedule.id,
            title=schedule.title,
            memo=schedule.memo,
            start=schedule.start,
            end=schedule.end,
            login_id=login_id,
        )
