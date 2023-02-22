from fastapi import FastAPI
from common.database import Database
from member.domain import admin, user

db = Database()
db.make_tables()
app = FastAPI()
