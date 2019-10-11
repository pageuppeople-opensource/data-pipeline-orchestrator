from sqlalchemy import desc, select
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from dpo.BaseObject import BaseObject
from dpo.Shared import Constants
from dpo.entities import ExecutionEntity, ExecutionStepEntity, ExecutionStepModelEntity
import uuid


class DataRepository(BaseObject):
    def __init__(self, db_engine, logger=None):
        super().__init__(logger)
        self.db_engine = db_engine
        self.session_maker = sessionmaker(bind=self.db_engine)

    def get_current_db_datetime_with_timezone(self):
        return self.db_engine.execute(select([func.now()])).fetchone()[0]

    def initialise_execution(self, execution_id=None):
        session = self.session_maker()

        data_pipeline_execution = ExecutionEntity()
        data_pipeline_execution.execution_id = execution_id if execution_id is not None else data_pipeline_execution.execution_id
        session.add(data_pipeline_execution)

        session.commit()
        return data_pipeline_execution

    def get_execution(self, execution_id):
        session = self.session_maker()
        result = session.query(ExecutionEntity) \
            .filter_by(execution_id=execution_id) \
            .first()
        session.close()
        return result

    def get_last_successful_execution(self):
        session = self.session_maker()
        result = session.query(ExecutionEntity) \
            .filter_by(status=Constants.ExecutionStatus.COMPLETED) \
            .order_by(desc(ExecutionEntity.updated_on)) \
            .order_by(desc(ExecutionEntity.created_on)) \
            .first()
        session.close()
        return result

    def initialise_execution_step(self, execution_id, step_name):
        session = self.session_maker()

        execution = session.query(ExecutionEntity) \
            .filter_by(execution_id=execution_id) \
            .one()
        execution.status = Constants.ExecutionStatus.IN_PROGRESS

        execution_step = ExecutionStepEntity(execution_id=execution_id,
                                             step_name=step_name)
        session.add(execution_step)

        session.commit()
        return execution_step

    def get_execution_step(self, execution_step_id):
        session = self.session_maker()
        result = session.query(ExecutionStepEntity) \
            .filter_by(execution_step_id=execution_step_id) \
            .one()
        session.close()
        return result

    def get_execution_steps(self, execution_id):
        session = self.session_maker()
        result = session.query(ExecutionStepEntity) \
            .filter_by(execution_id=execution_id)
        session.close()
        return result.all()

    def get_execution_step_models(self, step_id):
        session = self.session_maker()
        results = session.query(ExecutionStepModelEntity) \
            .filter_by(execution_step_id=step_id)
        session.close()
        return results.all()

    def save_execution_step_models(self, execution_step_id, model_checksums):
        session = self.session_maker()

        execution_step = session.query(ExecutionStepEntity) \
            .filter_by(execution_step_id=execution_step_id) \
            .one()
        execution_step.status = Constants.StepStatus.IN_PROGRESS

        for model_name, checksum in sorted(model_checksums.items()):
            execution_step_model = ExecutionStepModelEntity(execution_step_id=execution_step_id,
                                                            model_name=model_name,
                                                            checksum=checksum)
            session.add(execution_step_model)

        session.commit()

        return execution_step

    def complete_execution_step(self, execution_step_id, rows_processed):
        session = self.session_maker()

        execution_step = session.query(ExecutionStepEntity) \
            .filter_by(execution_step_id=execution_step_id) \
            .one()

        execution_step.status = Constants.StepStatus.COMPLETED
        execution_step.completed_on = self.get_current_db_datetime_with_timezone()
        execution_step.execution_time_ms \
            = (execution_step.completed_on - execution_step.started_on).total_seconds() * 1000
        execution_step.rows_processed = rows_processed

        session.commit()

        return execution_step

    def complete_execution(self, execution_id):
        session = self.session_maker()

        data_pipeline_execution = session.query(ExecutionEntity) \
            .filter_by(execution_id=execution_id) \
            .one()

        data_pipeline_execution.status = Constants.ExecutionStatus.COMPLETED
        data_pipeline_execution.completed_on = self.get_current_db_datetime_with_timezone()
        data_pipeline_execution.execution_time_ms \
            = (data_pipeline_execution.completed_on - data_pipeline_execution.started_on).total_seconds() * 1000

        session.commit()

        return data_pipeline_execution
