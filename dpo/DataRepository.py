from sqlalchemy import desc, select
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from dpo import Shared
from dpo.BaseObject import BaseObject
from dpo.Shared import Constants
from dpo.entities import ExecutionEntity
from dpo.entities import ExecutionModelEntity


class DataRepository(BaseObject):
    def __init__(self, db_engine, logger=None):
        super().__init__(logger)
        self.db_engine = db_engine
        self.session_maker = sessionmaker(bind=self.db_engine)

    def get_current_db_datetime_with_timezone(self):
        return self.db_engine.execute(select([func.now()])).fetchone()[0]

    def initialise_execution(self):
        session = self.session_maker()

        data_pipeline_execution = ExecutionEntity()
        session.add(data_pipeline_execution)

        session.commit()
        return data_pipeline_execution

    def get_execution(self, execution_id):
        session = self.session_maker()
        result = session.query(ExecutionEntity) \
            .filter_by(id=execution_id) \
            .first()
        session.close()
        return result

    def get_last_successful_execution(self):
        session = self.session_maker()
        result = session.query(ExecutionEntity) \
            .filter_by(status=Constants.DataPipelineExecutionStatus.COMPLETED) \
            .order_by(desc(ExecutionEntity.last_updated_on)) \
            .order_by(desc(ExecutionEntity.created_on)) \
            .first()
        session.close()
        return result

    def get_execution_models(self, execution_id, model_type):
        session = self.session_maker()
        results = session.query(ExecutionModelEntity) \
            .filter_by(execution_id=execution_id, type=model_type)
        session.close()
        return results.all()

    def save_execution_models(self, execution_id, model_type, model_checksums):
        session = self.session_maker()

        data_pipeline_execution = session.query(ExecutionEntity) \
            .filter_by(id=execution_id) \
            .one()

        data_pipeline_execution.status = \
            Constants.DataPipelineExecutionStatus.IN_PROGRESS
        for model, checksum in sorted(model_checksums.items()):
            model_checksum_entity = ExecutionModelEntity(execution_id=data_pipeline_execution.id,
                                                        type=model_type,
                                                        name=model,
                                                        checksum=checksum)
            session.add(model_checksum_entity)

        session.commit()

        return data_pipeline_execution

    def complete_execution(self, execution_id):
        session = self.session_maker()

        data_pipeline_execution = session.query(ExecutionEntity) \
            .filter_by(id=execution_id) \
            .one()

        data_pipeline_execution.status = Constants.DataPipelineExecutionStatus.COMPLETED
        data_pipeline_execution.last_updated_on = self.get_current_db_datetime_with_timezone()
        data_pipeline_execution.execution_time_ms \
            = (data_pipeline_execution.last_updated_on - data_pipeline_execution.created_on).total_seconds() * 1000

        session.commit()

        return data_pipeline_execution
