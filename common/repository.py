from abc import *

from common.database import Database


class Repository(metaclass=ABCMeta):
    def __init__(self, database: Database):
        self.db = database
        self.session = None

    def get_session(self):
        # 바뀌기 전껄로 하면 update할 때 session 달라서 안됨,,
        if not self.session:
            self.session = next(self.db.get_session())
        return self.session
