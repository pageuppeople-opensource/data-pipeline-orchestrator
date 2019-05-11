from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
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
                                     UUID(as_uuid=True),
                                     primary_key=True,
                                     default=uuid.uuid4())

    created_on = Column('created_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())

    updated_on = Column('updated_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.now())

    execution_step_id = Column('execution_step_id',
                               UUID(as_uuid=True),
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
