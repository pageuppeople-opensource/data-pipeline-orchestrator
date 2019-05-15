from sqlalchemy import Column, DateTime, BigInteger, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dpo.Shared import Constants
from dpo import Shared


class ExecutionEntity(Shared.BaseEntity):
    TABLE_NAME = 'execution'
    PRIMARY_KEY_COL_NAME = 'execution_id'

    __tablename__ = TABLE_NAME
    __table_args__ = {'schema': Constants.DATA_PIPELINE_ORCHESTRATOR_SCHEMA_NAME}

    execution_id = Column(PRIMARY_KEY_COL_NAME,
                          UUID(as_uuid=True),
                          primary_key=True,
                          default=uuid.uuid4)

    created_on = Column('created_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())

    updated_on = Column('updated_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now(),
                        onupdate=func.now())

    status = Column('status',
                    String(50),
                    nullable=False,
                    server_default=str(Constants.ExecutionStatus.INITIALISED))

    started_on = Column('started_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())

    completed_on = Column('completed_on',
                          DateTime(timezone=True),
                          nullable=True)

    execution_time_ms = Column('execution_time_ms',
                               BigInteger,
                               nullable=True)

    def __str__(self):
        return f'execution_id={self.execution_id}, ' \
               f'created_on={self.created_on}, ' \
               f'updated_on={self.updated_on}, ' \
               f'status={self.status}, ' \
               f'started_on={self.started_on}, ' \
               f'completed_on={self.completed_on}, ' \
               f'execution_time_ms={Shared.safe_format_number(self.execution_time_ms)}.'
