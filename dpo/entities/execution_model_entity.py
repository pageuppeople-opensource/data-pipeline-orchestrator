from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from dpo import Shared
from dpo.Shared import Constants
from dpo.entities import ExecutionEntity


class ExecutionModelEntity(Shared.BaseEntity):
    TABLE_NAME = 'execution_model'

    __tablename__ = TABLE_NAME
    __table_args__ = {'schema': Constants.DATA_PIPELINE_EXECUTION_SCHEMA_NAME}

    id = Column('id',
                Integer,
                primary_key=True,
                autoincrement=True)

    execution_id = Column('execution_id',
                          UUID(as_uuid=True),
                          ForeignKey(f'{Constants.DATA_PIPELINE_EXECUTION_SCHEMA_NAME}.'
                                     f'{ExecutionEntity.TABLE_NAME}.'
                                     f'{ExecutionEntity.PRIMARY_KEY_COL_NAME}'),
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

    type = Column('type',
                  String(100),
                  nullable=False)

    name = Column('name',
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
            f'type={self.type}, ' \
            f'name={self.name}, ' \
            f'checksum={self.checksum}.'
