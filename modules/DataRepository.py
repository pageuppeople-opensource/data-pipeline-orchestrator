from modules.BaseObject import BaseObject
from modules.entities.DataPipelineExecutionEntity import DataPipelineExecutionEntity
from modules.entities.ModelChecksumEntity import ModelChecksumEntity
from modules.Shared import Constants
from modules import Shared


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

    def finish_execution(self, execution_id, model_checksums_by_folders):
        session = self.session_maker()

        data_pipeline_execution = session.query(DataPipelineExecutionEntity) \
            .filter_by(id=execution_id) \
            .one()
        data_pipeline_execution.status = Constants.DataPipelineExecutionStatus.COMPLETED_SUCCESSFULLY

        for folder_name, model_checksums in model_checksums_by_folders.items():
            for model, checksum in sorted(set(model_checksums.items())):
                model_checksum = ModelChecksumEntity(execution_id=data_pipeline_execution.id,
                                                     type=folder_name,
                                                     name=model,
                                                     checksum=checksum)
                session.add(model_checksum)

        session.commit()
        return data_pipeline_execution
