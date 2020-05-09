"""empty message

Revision ID: 50ffce28d70e
Revises: b55e143b08a7
Create Date: 2020-04-24 09:21:46.265591

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '50ffce28d70e'
down_revision = 'b55e143b08a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_expression_ibfk_2', 'user_expression', type_='foreignkey')
    op.drop_constraint('user_expression_ibfk_1', 'user_expression', type_='foreignkey')
    op.drop_index('user_id', table_name='user_expression')
    op.drop_index('expression_id', table_name='user_expression')
    op.drop_table('user_expression')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_expression',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('expression_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_index('user_id', 'user_expression', ['user_id', 'expression_id'], unique=True)
    # ### end Alembic commands ###
