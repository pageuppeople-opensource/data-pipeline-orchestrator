from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from modules import Shared
from modules.Shared import Constants
from modules.entities import DataPipelineExecutionEntity

TABLE_NAME = 'model_checksum'


class ModelChecksumEntity(Shared.BaseEntity):
    __tablename__ = TABLE_NAME
    __table_args__ = {'schema': Constants.DATA_PIPELINE_EXECUTION_SCHEMA_NAME}

    id = Column('id',
                Integer,
                primary_key=True,
                autoincrement=True)

    execution_id = Column('execution_id',
                          UUID(as_uuid=True),
                          ForeignKey(f'{Constants.DATA_PIPELINE_EXECUTION_SCHEMA_NAME}.'
                                     f'{DataPipelineExecutionEntity.TABLE_NAME}.'
                                     f'{DataPipelineExecutionEntity.PRIMARY_KEY_COL_NAME}'),
                          nullable=False)

    created_on = Column('created_on',
                        DateTime(timezone=True),
                        nullable=False,
                        server_default=func.now())

    last_updated_on = Column('last_updated_on',
                             DateTime(timezone=True),
                             nullable=False,
                             server_default=func.now(),
                             onupdate=func.now())

    foldername = Column('foldername',
                        String(100),
                        nullable=False)

    filename = Column('filename',
                      String(250),
                      nullable=False)

    checksum = Column('checksum',
                      String(100),
                      nullable=False)

    def __str__(self):
        return f'id={self.id}, ' \
            f'execution_id={self.execution_id}, ' \
            f'created_on={self.created_on}, ' \
            f'last_updated_on={self.last_updated_on}, ' \
            f'filename={self.filename}, ' \
            f'checksum={self.checksum}.'
