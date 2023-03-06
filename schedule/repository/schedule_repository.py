from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select, extract, or_, and_

from common.repository import Repository
from member.domain.user import User
from schedule.domain.schedule import Schedule
from schedule.enum.status import Status


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

    def find_all_by_period_weekly(self, user) -> List[Schedule]:
        session = self.get_session()
        today = datetime.now().date()
        # Calculate the day of the week as an integer (0=Monday, 1=Tuesday, etc.)
        weekday = today.weekday()
        start_date = today - timedelta(days=weekday)
        end_date = today + timedelta(days=(7 - weekday - 1))
        query = (
            select(Schedule)
            .filter(
                or_(
                    Schedule.start.between(start_date, end_date),
                    Schedule.status == Status.IN_PROGRESS.value,
                ),
                Schedule.user == user,
            )
            .order_by(Schedule.start, Schedule.end)
        )
        return session.scalars(query).all()

    def find_all_by_period_monthly(self, user) -> List[Schedule]:
        session = self.get_session()
        query = (
            select(Schedule)
            .filter(
                self._is_in_this_month(),
                Schedule.user == user,
            )
            .order_by(Schedule.start, Schedule.end)
        )
        return session.scalars(query).all()

    def find_all_by_user(self, user) -> List[Schedule]:
        session = self.get_session()
        query = (
            select(Schedule).filter_by(user=user).order_by(Schedule.start, Schedule.end)
        )
        return session.scalars(query).all()

    def _is_in_this_month(self):
        today = datetime.now().date()
        return or_(
            and_(
                extract("month", Schedule.start) == today.month,
                extract("year", Schedule.start) == today.year,
            ),
            and_(
                extract("month", Schedule.end) == today.month,
                extract("year", Schedule.end) == today.year,
            ),
            Schedule.status == Status.IN_PROGRESS.value,
        )
