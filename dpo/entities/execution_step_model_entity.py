from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
import uuid
from dpo import Shared
from dpo.Shared import Constants
from dpo.entities import ExecutionEntity, ExecutionStepEntity
from sqlalchemy.inspection import inspect


class ExecutionStepModelEntity(Shared.BaseEntity):
    TABLE_NAME = 'execution_step_model'
    PRIMARY_KEY_COL_NAME = 'execution_step_model_id'

    __tablename__ = TABLE_NAME
    __table_args__ = {'schema': Constants.DATA_PIPELINE_ORCHESTRATOR_SCHEMA_NAME}

    execution_step_model_id = Column(PRIMARY_KEY_COL_NAME,
                                     String(250),
                                     primary_key=True,
                                     default=f"{uuid.uuid4()}")

    created_on = Column('created_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.timezone("UTC", func.getdate()))

    updated_on = Column('updated_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.timezone("UTC", func.getdate()),
                        onupdate=func.timezone("UTC", func.getdate()))

    execution_step_id = Column('execution_step_id',
                               String(250),
                               ForeignKey(f'{Constants.DATA_PIPELINE_ORCHESTRATOR_SCHEMA_NAME}.'
                                          f'{inspect(ExecutionStepEntity).tables[0].name}.'
                                          f'{inspect(ExecutionStepEntity).primary_key[0].name}'),
                               nullable=False)

    model_name = Column('model_name',
                        String(250),
                        nullable=False)

    checksum = Column('checksum',
                      String(100),
                      nullable=False)

    def __str__(self):
        return f'execution_step_model_id={self.execution_step_model_id}, ' \
               f'created_on={self.created_on}, ' \
               f'updated_on={self.updated_on}, ' \
               f'execution_step_id={self.execution_step_id}, ' \
               f'model_name={self.model_name}, ' \
               f'checksum={self.checksum}.'
