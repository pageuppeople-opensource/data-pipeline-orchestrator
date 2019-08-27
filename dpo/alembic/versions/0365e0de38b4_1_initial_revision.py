"""1 initial revision

Revision ID: 0365e0de38b4
Revises: 
Create Date: 2019-08-27 09:45:24.073834

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0365e0de38b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # create schema
    op.execute("CREATE SCHEMA IF NOT EXISTS dpo")

    # create tables
    op.create_table('execution',
                    sa.Column('execution_id', sa.String(length=250), nullable=False),
                    sa.Column('created_on', sa.DateTime(timezone=True),
                              server_default=sa.text('timezone("UTC", getdate())'), nullable=False),
                    sa.Column('updated_on', sa.DateTime(timezone=True),
                              server_default=sa.text('timezone("UTC", getdate())'), nullable=False),
                    sa.Column('status', sa.String(length=50), server_default='INITIALISED', nullable=False),
                    sa.Column('started_on', sa.DateTime(timezone=True),
                              server_default=sa.text('timezone("UTC", getdate())'), nullable=False),
                    sa.Column('completed_on', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('execution_time_ms', sa.BigInteger(), nullable=True),
                    sa.PrimaryKeyConstraint('execution_id'),
                    schema='dpo'
                    )
    op.create_table('execution_step',
                    sa.Column('execution_step_id', sa.String(length=250), nullable=False),
                    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('timezone("UTC", getdate())'),
                              nullable=False),
                    sa.Column('updated_on', sa.DateTime(timezone=True), server_default=sa.text('timezone("UTC", getdate())'),
                              nullable=False),
                    sa.Column('execution_id', sa.String(length=250), nullable=False),
                    sa.Column('step_name', sa.String(length=100), nullable=False),
                    sa.Column('status', sa.String(length=50), server_default='INITIALISED', nullable=False),
                    sa.Column('started_on', sa.DateTime(timezone=True), server_default=sa.text('timezone("UTC", getdate())'),
                              nullable=False),
                    sa.Column('completed_on', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('execution_time_ms', sa.BigInteger(), nullable=True),
                    sa.Column('rows_processed', sa.BigInteger(), nullable=True),
                    sa.ForeignKeyConstraint(['execution_id'], ['dpo.execution.execution_id'], ),
                    sa.PrimaryKeyConstraint('execution_step_id'),
                    schema='dpo'
                    )
    op.create_table('execution_step_model',
                    sa.Column('execution_step_model_id', sa.String(length=250), nullable=False),
                    sa.Column('created_on', sa.DateTime(timezone=True), server_default=sa.text('timezone("UTC", getdate())'),
                              nullable=False),
                    sa.Column('updated_on', sa.DateTime(timezone=True), server_default=sa.text('timezone("UTC", getdate())'),
                              nullable=False),
                    sa.Column('execution_step_id', sa.String(length=250), nullable=False),
                    sa.Column('model_name', sa.String(length=250), nullable=False),
                    sa.Column('checksum', sa.String(length=100), nullable=False),
                    sa.ForeignKeyConstraint(['execution_step_id'], ['dpo.execution_step.execution_step_id'], ),
                    sa.PrimaryKeyConstraint('execution_step_model_id'),
                    schema='dpo'
                    )


def downgrade():
    # drop tables
    op.drop_table('execution_step_model', schema='dpo')
    op.drop_table('execution_model', schema='dpo')
    op.drop_table('execution', schema='dpo')

    # drop schema
    op.execute("DROP SCHEMA IF EXISTS rdl")
