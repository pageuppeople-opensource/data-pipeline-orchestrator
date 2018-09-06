import logging
from sqlalchemy import desc
from modules.DataPipelineExecutionEntity import DataPipelineExecutionEntity, Base
from modules import Shared
from modules import Constants


class DataPipelineExecutionRepository(object):

    def __init__(self, session_maker, logger=None):
        self.session_maker = session_maker
        self.logger = logger or logging.getLogger(__name__)
        Shared.configure_logging(self.logger, Shared.args.log_level)

    def create_schema(self, engine):
        engine.execute(f'CREATE SCHEMA IF NOT EXISTS {Constants.DataPipelineExecutionSchemaName}')
        Base.metadata.create_all(engine)

    def start_new(self):
        session = self.session_maker()
        data_pipeline_execution = DataPipelineExecutionEntity()
        session.add(data_pipeline_execution)
        session.commit()
        return data_pipeline_execution

    def get_last_successful_data_load_execution(self):
        session = self.session_maker()
        return session.query(DataPipelineExecutionEntity)\
            .filter_by(status=Constants.DataPipelineExecutionStatus.COMPLETED_SUCCESSFULLY)\
            .order_by(desc(DataPipelineExecutionEntity.created_on))\
            .order_by(desc(DataPipelineExecutionEntity.last_updated_on))\
            .first()

