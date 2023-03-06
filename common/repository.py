from abc import *

from common.database import Database


class Repository(metaclass=ABCMeta):
    def __init__(self, database: Database):
        self.db = database
        self.session = None

    def get_session(self):
        if not self.session:
            self.session = next(self.db.get_session())
        return self.session
