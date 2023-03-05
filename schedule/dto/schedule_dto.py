from datetime import datetime

from pydantic import BaseModel


class ScheduleCreateDto(BaseModel):
    title: str
    memo: str
    # yyyymmddhhmm
    start: str
    end: str


class ScheduleUpdateCreateDto(ScheduleCreateDto):
    id: int
