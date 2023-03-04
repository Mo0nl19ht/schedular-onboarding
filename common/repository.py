from abc import *

from common.database import Database


class Repository(metaclass=ABCMeta):
    def __init__(self, database: Database):
        self.db = database

    def get_session(self):
        # singelton으로 세션을 사용하면 동시성 문제 발생 가능함
        # if not self.session:
        #     self.session = next(self.db.get_session())
        # return self.session
        return next(self.db.get_session())
