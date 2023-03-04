from datetime import datetime

from pydantic import BaseModel


class ScheduleDto(BaseModel):
    title: str
    memo: str
    # yyyymmddhhmm
    start: str
    end: str


class ScheduleUpdateDto(ScheduleDto):
    id: int
