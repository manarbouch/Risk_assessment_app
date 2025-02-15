"""Added RiskAssessment model

Revision ID: 38198fa09405
Revises: f7fa7264f470
Create Date: 2024-11-27 18:42:59.979783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38198fa09405'
down_revision = 'f7fa7264f470'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('risk_assessment')
    op.drop_table('users')
    op.drop_table('risk_assessments')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    sa.Column('password', sa.VARCHAR(length=200), nullable=False),
    sa.Column('completed_questionnaire', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('risk_assessments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('goal', sa.VARCHAR(length=50), nullable=False),
    sa.Column('time_horizon', sa.VARCHAR(length=50), nullable=False),
    sa.Column('reaction', sa.VARCHAR(length=50), nullable=False),
    sa.Column('savings_rate', sa.VARCHAR(length=50), nullable=False),
    sa.Column('experience', sa.VARCHAR(length=50), nullable=False),
    sa.Column('risk_score', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('password', sa.VARCHAR(length=200), nullable=False),
    sa.Column('completed_questionnaire', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('risk_assessment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('goal', sa.VARCHAR(length=50), nullable=False),
    sa.Column('time_horizon', sa.VARCHAR(length=50), nullable=False),
    sa.Column('reaction', sa.VARCHAR(length=50), nullable=False),
    sa.Column('savings_rate', sa.VARCHAR(length=50), nullable=False),
    sa.Column('experience', sa.VARCHAR(length=50), nullable=False),
    sa.Column('risk_score', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
