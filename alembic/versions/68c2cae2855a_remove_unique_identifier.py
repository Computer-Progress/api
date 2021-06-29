"""remove unique identifier

Revision ID: 68c2cae2855a
Revises: 5db2d9c38f21
Create Date: 2021-06-29 02:43:19.202721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68c2cae2855a'
down_revision = '5db2d9c38f21'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accuracy_value', 'value',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('cpu', 'frequency',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('cpu', 'tdp',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('cpu', 'gflops',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('gpu', 'tdp',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('gpu', 'gflops',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('model', 'hardware_burden',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('model', 'gflops',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('model', 'multiply_adds',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.drop_constraint('model_identifier_key', 'model', type_='unique')
    op.drop_constraint('paper_identifier_key', 'paper', type_='unique')
    op.alter_column('tpu', 'tdp',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    op.alter_column('tpu', 'gflops',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=3),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tpu', 'gflops',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('tpu', 'tdp',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.create_unique_constraint('paper_identifier_key', 'paper', ['identifier'])
    op.create_unique_constraint('model_identifier_key', 'model', ['identifier'])
    op.alter_column('model', 'multiply_adds',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('model', 'gflops',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('model', 'hardware_burden',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('gpu', 'gflops',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('gpu', 'tdp',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('cpu', 'gflops',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('cpu', 'tdp',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('cpu', 'frequency',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('accuracy_value', 'value',
               existing_type=sa.Float(precision=3),
               type_=sa.REAL(),
               existing_nullable=True)
    # ### end Alembic commands ###