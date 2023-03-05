from datetime import datetime
from typing import List

from fastapi import Depends
from sqlalchemy import select

from common.database import Database
from common.repository import Repository
from member.domain.user import User
from schedule.domain.schedule import Schedule


class ScheduleRepository(Repository):
    def create(self, schedule: Schedule) -> Schedule:
        try:
            session = self.get_session()
            session.add(schedule)
            session.commit()
            session.refresh(schedule)
            return schedule
        except Exception as e:
            session.rollback()
            raise e

    def find_by_start_and_end(self, start: datetime, end: datetime, user_id: int):
        session = self.get_session()
        query = select(Schedule).filter_by(start=start, end=end, user_id=user_id)
        return session.scalar(query)

    def find_by_id(self, id: int):
        session = self.get_session()
        query = select(Schedule).filter_by(id=id)
        return session.scalar(query)

    def update(self, schedule: Schedule) -> Schedule:
        try:
            session = self.get_session()
            session.commit()
            session.refresh(schedule)
            return schedule
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, schedule: Schedule):
        try:
            session = self.get_session()
            session.delete(schedule)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def find_all_by_status(self, status_value, user: User) -> List[Schedule]:
        session = self.get_session()
        query = (
            select(Schedule)
            .filter_by(status=status_value, user=user)
            .order_by(Schedule.start, Schedule.end)
        )
        return session.scalars(query).all()
