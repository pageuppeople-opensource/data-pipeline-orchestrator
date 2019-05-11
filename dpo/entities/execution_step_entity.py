from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dpo import Shared
from dpo.Shared import Constants
from dpo.entities import ExecutionEntity
from sqlalchemy.inspection import inspect


class ExecutionStepEntity(Shared.BaseEntity):
    TABLE_NAME = 'execution_step'
    PRIMARY_KEY_COL_NAME = 'execution_step_id'

    __tablename__ = TABLE_NAME
    __table_args__ = {'schema': Constants.DATA_PIPELINE_ORCHESTRATOR_SCHEMA_NAME}

    execution_step_id = Column(PRIMARY_KEY_COL_NAME,
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

    execution_id = Column('execution_id',
                          UUID(as_uuid=True),
                          ForeignKey(f'{Constants.DATA_PIPELINE_ORCHESTRATOR_SCHEMA_NAME}.'
                                     f'{inspect(ExecutionEntity).tables[0].name}.'
                                     f'{inspect(ExecutionEntity).primary_key[0].name}'),
                          nullable=False)

    step_name = Column('step_name',
                       String(100),
                       nullable=False)

    status = Column('status',
                    String(50),
                    nullable=False,
                    server_default=str(Constants.StepStatus.INITIALISED))

    started_on = Column('started_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())

    completed_on = Column('completed_on',
                          DateTime(timezone=True),
                          nullable=True)

    execution_time_ms = Column('execution_time_ms',
                               Integer,
                               nullable=True)

    def __str__(self):
        return f'execution_step_id={self.execution_step_id}, ' \
               f'created_on={self.created_on}, ' \
               f'updated_on={self.updated_on}, ' \
               f'execution_id={self.execution_id}, ' \
               f'step_name={self.step_name}, ' \
               f'status={self.status}, ' \
               f'started_on={self.started_on}, ' \
               f'completed_on={self.completed_on}, ' \
               f'execution_time_ms={self.execution_time_ms}.'
