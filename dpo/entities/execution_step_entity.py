from sqlalchemy import Column, DateTime, BigInteger, String, ForeignKey
from sqlalchemy.sql import func
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

    execution_id = Column('execution_id',
                          String(250),
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
                        server_default=func.timezone("UTC", func.getdate()))

    completed_on = Column('completed_on',
                          DateTime(timezone=True),
                          nullable=True)

    execution_time_ms = Column('execution_time_ms',
                               BigInteger,
                               nullable=True)

    rows_processed = Column('rows_processed',
                            BigInteger,
                            nullable=True)

    def __str__(self):
        return f'execution_id={self.execution_id}, ' \
               f'execution_step_id={self.execution_step_id}, ' \
               f'created_on={self.created_on}, ' \
               f'updated_on={self.updated_on}, ' \
               f'step_name={self.step_name}, ' \
               f'status={self.status}, ' \
               f'started_on={self.started_on}, ' \
               f'completed_on={self.completed_on}, ' \
               f'execution_time_ms={Shared.safe_format_number(self.execution_time_ms)}, ' \
               f'rows_processed={Shared.safe_format_number(self.rows_processed)}.'
