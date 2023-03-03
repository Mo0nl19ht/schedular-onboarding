from fastapi import FastAPI
from common.database import Database
from member.controller.user_controller import UserController
from member.domain import admin, user, member
from member.repository.user_repository import UserRepository
from member.service.user_service import UserService

db = Database()
db.make_tables()
app = FastAPI()

user_repository = UserRepository(db)
user_service = UserService(user_repository)
user_controller = UserController(user_service)

app.include_router(user_controller.router)
