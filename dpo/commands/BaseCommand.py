from sqlalchemy import create_engine
from dpo.DataRepository import DataRepository
from dpo.BaseObject import BaseObject


class BaseCommand(BaseObject):
    def __init__(self, db_connection_string, logger=None):
        super().__init__(logger)
        self.db_engine = create_engine(db_connection_string, echo=False)
        self.repository = DataRepository(self.db_engine)

    def execute(self):
        raise NotImplementedError()

    def output(self, *args):
        raise NotImplementedError()
