from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base


class Database:
    name = "mysql+pymysql"
    user = "member"
    password = "member"
    host = "localhost"
    db_name = "pilot"
    port = "3306"

    def __init__(self):
        database_url = f"{self.name}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.engine = create_engine(database_url)

    def get_session(self):
        session = sessionmaker(bind=self.engine)
        with session() as db:
            yield db


db = Database()
Base = declarative_base()
