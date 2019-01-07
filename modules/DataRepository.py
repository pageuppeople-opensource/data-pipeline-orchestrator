from modules.BaseObject import BaseObject
from modules.DataPipelineExecutionEntity import DataPipelineExecutionEntity
from modules.ModelChecksumEntity import ModelChecksumEntity
from modules.Shared import Constants
from modules import Shared


class DataRepository(BaseObject):
    def __init__(self, session_maker, logger=None):
        super().__init__(logger)
        self.session_maker = session_maker

    def ensure_schema_exists(self, engine):
        engine.execute(f'CREATE SCHEMA IF NOT EXISTS {Constants.DATA_PIPELINE_EXECUTION_SCHEMA_NAME}')
        Shared.BaseEntity.metadata.create_all(engine)

    def start_new(self):
        session = self.session_maker()

        data_pipeline_execution = DataPipelineExecutionEntity()
        session.add(data_pipeline_execution)

        session.commit()
        return data_pipeline_execution

    def finish_existing(self, execution_id, file_checksums):
        session = self.session_maker()

        data_pipeline_execution = session.query(DataPipelineExecutionEntity)\
            .filter_by(id=execution_id)\
            .one()
        data_pipeline_execution.status = Constants.DataPipelineExecutionStatus.COMPLETED_SUCCESSFULLY

        for file_name, file_hash in sorted(set(file_checksums.items())):
            model_hash = ModelChecksumEntity(execution_id=data_pipeline_execution.id,
                                             filename=file_name,
                                             checksum=file_hash)
            session.add(model_hash)

        session.commit()
        return data_pipeline_execution


