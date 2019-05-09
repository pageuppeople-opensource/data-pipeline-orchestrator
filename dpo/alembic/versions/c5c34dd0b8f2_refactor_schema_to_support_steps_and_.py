"""refactor schema to support steps and stats

Revision ID: c5c34dd0b8f2
Revises: fe9eed6d812f
Create Date: 2019-05-08 13:48:24.073834

"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c5c34dd0b8f2'
down_revision = 'fe9eed6d812f'
branch_labels = None
depends_on = None


def upgrade():
    # mark existing tables with old revision
    op.execute('ALTER TABLE dpo.execution RENAME TO fe9eed6d812f_execution')
    op.execute('ALTER TABLE dpo.execution_model RENAME TO fe9eed6d812f_execution_model')

    # create new schema tables
    op.create_table('execution',
                    sa.Column('execution_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('created_on', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_on', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('status', sa.String(length=50), server_default='INITIALISED', nullable=False),
                    sa.Column('started_on', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('completed_on', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('execution_time_ms', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('execution_id'),
                    schema='dpo'
                    )
    op.create_table('execution_step',
                    sa.Column('execution_step_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('updated_on', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('execution_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('step_name', sa.String(length=100), nullable=False),
                    sa.Column('status', sa.String(length=50), server_default='INITIALISED', nullable=False),
                    sa.Column('started_on', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('completed_on', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('execution_time_ms', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['execution_id'], ['dpo.execution.execution_id'], ),
                    sa.PrimaryKeyConstraint('execution_step_id'),
                    schema='dpo'
                    )
    op.create_table('execution_step_model',
                    sa.Column('execution_step_model_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('updated_on', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('execution_step_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('model_name', sa.String(length=250), nullable=False),
                    sa.Column('checksum', sa.String(length=100), nullable=False),
                    sa.ForeignKeyConstraint(['execution_step_id'], ['dpo.execution_step.execution_step_id'], ),
                    sa.PrimaryKeyConstraint('execution_step_model_id'),
                    schema='dpo'
                    )

    # move data from old tables to new tables
    op.execute(
        '''
        INSERT INTO dpo.execution (
            execution_id, created_on, updated_on, status, started_on, completed_on, execution_time_ms
        )
        SELECT
            id, created_on, last_updated_on, status, created_on, last_updated_on, execution_time_ms
        FROM dpo.fe9eed6d812f_execution
        ''')
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.execute(
        '''
        INSERT INTO dpo.execution_step (
            execution_step_id, execution_id, created_on, updated_on,
            step_name, status, started_on, completed_on, execution_time_ms
        )
        SELECT
            uuid_generate_v4() AS execution_step_id
            , e.id AS execution_id
            , (select min(cm.created_on) from dpo.fe9eed6d812f_execution_model cm where cm.execution_id = e.id and cm.type = m.type) AS created_on
            , (select max(um.last_updated_on) from dpo.fe9eed6d812f_execution_model um where um.execution_id = e.id and um.type = m.type) AS updated_on
            , m.type AS step_name
            , 'UNKNOWN' AS status
            , (select min(sm.created_on) from dpo.fe9eed6d812f_execution_model sm where sm.execution_id = e.id and sm.type = m.type) AS started_on
            , NULL AS completed_on
            , NULL AS execution_time_ms
        FROM  dpo.fe9eed6d812f_execution e
        JOIN  dpo.fe9eed6d812f_execution_model m on e.id = m.execution_id
        GROUP BY e.id, e.status, e.created_on, m.type
        ORDER BY e.created_on, m.type
        ''')
    op.execute(
        '''
        INSERT INTO dpo.execution_step_model (
            execution_step_model_id, execution_step_id, created_on, updated_on, model_name, checksum
        )
        SELECT
            uuid_generate_v4() AS execution_step_model_id
            , es.execution_step_id, em.created_on, em.last_updated_on, em.name, em.checksum
        FROM dpo.execution_step es
        JOIN dpo.fe9eed6d812f_execution_model em
             ON  em.execution_id = es.execution_id
             AND em.type = es.step_name
        ORDER BY em.created_on
        ''')

    # optinally, drop old tables
    # op.drop_table('fe9eed6d812f_execution_model', schema='dpo')
    # op.drop_table('fe9eed6d812f_execution', schema='dpo')


def downgrade():
    op.drop_table('execution_step_model', schema='dpo')
    op.drop_table('execution_step', schema='dpo')
    op.drop_table('execution', schema='dpo')
    op.execute('ALTER TABLE dpo.fe9eed6d812f_execution RENAME TO execution')
    op.execute('ALTER TABLE dpo.fe9eed6d812f_execution_model RENAME TO execution_model')
