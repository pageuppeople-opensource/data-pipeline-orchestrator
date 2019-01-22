from sqlalchemy import desc

from modules import Shared
from modules.BaseObject import BaseObject
from modules.Shared import Constants
from modules.entities.DataPipelineExecutionEntity import DataPipelineExecutionEntity
from modules.entities.ModelChecksumEntity import ModelChecksumEntity


class DataRepository(BaseObject):
    def __init__(self, session_maker, logger=None):
        super().__init__(logger)
        self.session_maker = session_maker

    def ensure_schema_exists(self, engine):
        engine.execute(f'CREATE SCHEMA IF NOT EXISTS {Constants.DATA_PIPELINE_EXECUTION_SCHEMA_NAME}')
        Shared.BaseEntity.metadata.create_all(engine)

    def start_execution(self):
        session = self.session_maker()

        data_pipeline_execution = DataPipelineExecutionEntity()
        session.add(data_pipeline_execution)

        session.commit()
        return data_pipeline_execution

    def get_last_successful_models(self, model_type):
        last_successful_models = {}
        session = self.session_maker()

        last_successful_execution = session.query(DataPipelineExecutionEntity) \
            .filter_by(status=Constants.DataPipelineExecutionStatus.COMPLETED_SUCCESSFULLY) \
            .order_by(desc(DataPipelineExecutionEntity.last_updated_on)) \
            .order_by(desc(DataPipelineExecutionEntity.created_on)) \
            .first()

        if last_successful_execution is None:
            return last_successful_models

        previous_model_checksums = session.query(ModelChecksumEntity) \
            .filter_by(execution_id=last_successful_execution.id, type=model_type)

        for model_checksum_entity in previous_model_checksums:
            last_successful_models[model_checksum_entity.name] = model_checksum_entity.checksum

        return last_successful_models

    def save_execution_progress(self, execution_id, model_type, model_checksums):
        session = self.session_maker()

        data_pipeline_execution = session.query(DataPipelineExecutionEntity) \
            .filter_by(id=execution_id) \
            .one()
        data_pipeline_execution.status = Constants.DataPipelineExecutionStatus.IN_PROGRESS

        for model, checksum in sorted(model_checksums.items()):
            model_checksum_entity = ModelChecksumEntity(execution_id=data_pipeline_execution.id,
                                                        type=model_type,
                                                        name=model,
                                                        checksum=checksum)
            session.add(model_checksum_entity)

        session.commit()
        return data_pipeline_execution

    def finish_execution(self, execution_id):
        session = self.session_maker()

        data_pipeline_execution = session.query(DataPipelineExecutionEntity) \
            .filter_by(id=execution_id) \
            .one()
        data_pipeline_execution.status = Constants.DataPipelineExecutionStatus.COMPLETED_SUCCESSFULLY

        session.commit()
        return data_pipeline_execution
