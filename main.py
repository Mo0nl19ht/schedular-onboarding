from fastapi import FastAPI
from common.database import Database
from member.controller.admin_controller import AdminController
from member.controller.user_controller import UserController
from member.repository.admin_repository import AdminRepository
from member.repository.user_repository import UserRepository
from member.service.admin_service import AdminService
from member.service.user_service import UserService
from schedule.controller.schedule_controller import ScheduleController
from schedule.repository.schedule_repository import ScheduleRepository
from schedule.service.schedule_service import ScheduleService

# to ORM mapping
from schedule.domain import schedule
from member.domain import member, admin, user

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


app.include_router(user_controller.router)
app.include_router(schedule_controller.router)
app.include_router(admin_controller.router)
