from datetime import datetime

from fastapi import FastAPI
from common.database import Database
from member.controller.admin_controller import AdminController
from member.controller.user_controller import UserController
from member.domain import admin, user, member
from member.domain.user import User
from member.repository.admin_repository import AdminRepository
from member.repository.user_repository import UserRepository
from member.service.admin_service import AdminService
from member.service.user_service import UserService
from schedule.controller.schedule_controller import ScheduleController
from schedule.domain.schedule import Schedule
from schedule.domain.status_enum import Status
from schedule.repository.schedule_repository import ScheduleRepository
from schedule.service.schedule_service import ScheduleService

db = Database()
db.make_tables()
app = FastAPI()

user_repository = UserRepository(db)
user_service = UserService(user_repository)
user_controller = UserController(user_service)

admin_repository = AdminRepository(db)
admin_service = AdminService(admin_repository)
admin_controller = AdminController(admin_service)

schedule_repository = ScheduleRepository(db)
schedule_service = ScheduleService(schedule_repository, user_repository)
schedule_controller = ScheduleController(schedule_service)
#
# user = User(
#     login_id="mm",
#     email="123@mai.",
#     name="123",
#     hashed_password="ASda",
# )
# user = user_repository.create(user)

# schedule = Schedule(
#     title="this is title",
#     memo="memooemoemoemo",
#     start=datetime(2023, 3, 3, 14, 00),
#     end=datetime(2023, 3, 3, 14, 30),
#     user=user,
# )
# .create(schedule)


app.include_router(user_controller.router)
app.include_router(schedule_controller.router)
app.include_router(admin_controller.router)
