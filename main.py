from datetime import datetime

from fastapi import FastAPI
from common.database import Database
from member.controller.user_controller import UserController
from member.domain import admin, user, member
from member.repository.user_repository import UserRepository
from member.service.user_service import UserService
from schedule.domain.schedule import Schedule
from schedule.domain.status_enum import Status
from schedule.repository.schedule_repository import ScheduleRepository

db = Database()
db.make_tables()
app = FastAPI()

user_repository = UserRepository(db)
user_service = UserService(user_repository)
user_controller = UserController(user_service)

schedule_repository = ScheduleRepository(db)
# schedule = Schedule(
#     title="this is title",
#     memo="memooemoemoemo",
#     start=datetime(2023, 3, 3, 14, 00),
#     end=datetime(2023, 3, 3, 14, 30),
# )
# schedule_repository.create(schedule)

app.include_router(user_controller.router)
