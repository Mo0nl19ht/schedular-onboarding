from datetime import datetime

from fastapi import Depends
from sqlalchemy import select

from common.database import Database
from common.repository import Repository
from schedule.domain.schedule import Schedule


class ScheduleRepository(Repository):
    def create(self, schedule: Schedule) -> Schedule:
        session = self.get_session()
        session.add(schedule)
        session.commit()
        session.refresh(schedule)
        return schedule

    def find_by_start_and_end(self, start: datetime, end: datetime):
        session = self.get_session()
        query = select(Schedule).filter_by(start=start, end=end)
        return session.scalar(query)
