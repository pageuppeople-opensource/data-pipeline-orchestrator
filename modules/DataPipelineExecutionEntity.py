from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from modules import Constants

Base = declarative_base()


class DataPipelineExecutionEntity(Base):

    __tablename__ = 'data_pipeline_execution'
    __table_args__ = {'schema': Constants.dataPipelineExecutionSchemaName}

    id = Column('id',
                Integer,
                primary_key=True,
                autoincrement=True)

    uuid = Column('uuid',
                  UUID(as_uuid=True),
                  unique=True,
                  nullable=False,
                  default=uuid.uuid4())

    # or just one identifier?
    # id = Column('id',
    #             UUID(as_uuid=True),
    #             unique=True,
    #             primary_key=True,
    #             default=uuid.uuid4())

    created_on = Column('created_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())

    last_updated_on = Column('last_updated_on',
                             DateTime(timezone=True),
                             nullable=False,
                             server_default=func.now(),
                             onupdate=func.now())

    # unused for now, for future use
    execution_time_ms = Column('execution_time_ms',
                               Integer,
                               nullable=True)

    # can map to a status lookup table. for now, using the below status
    # 1 = started
    # 0 = completed successfully (sort of like exit code 0 of a process)
    # 2,3,4,5... can be all custom statuses built and uses as we proceed
    status = Column('status',
                    Integer,
                    nullable=False,
                    server_default=str(Constants.DataPipelineExecutionStatus.STARTED))

    def __str__(self):
        return f'id={self.id}, ' \
               f'uuid={self.uuid}, ' \
               f'created_on={self.created_on}, ' \
               f'last_updated_on={self.last_updated_on}, ' \
               f'execution_time_ms={self.execution_time_ms}, ' \
               f'status={self.status}.'
