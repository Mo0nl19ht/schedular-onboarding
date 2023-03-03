from common.repository import Repository
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
            return e
