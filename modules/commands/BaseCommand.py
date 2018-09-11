import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules import Shared
from modules.DataPipelineExecutionRepository import DataPipelineExecutionRepository


class BaseCommand(object):
    def __init__(self, db_connection_string, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        Shared.write_output(self.logger, Shared.args.verbose)
        self.db_engine = create_engine(db_connection_string, echo=Shared.args.verbose)
        self.session_maker = sessionmaker(bind=self.db_engine)
        self.repository = DataPipelineExecutionRepository(self.session_maker)
        self.repository.create_schema(engine=self.db_engine)
