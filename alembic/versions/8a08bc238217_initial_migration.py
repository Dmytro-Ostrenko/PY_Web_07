"""initial migration

Revision ID: 8a08bc238217
Revises: 
Create Date: 2024-02-19 18:45:50.702751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a08bc238217'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    op.drop_table('grades')
    op.drop_table('lectors')
    op.drop_table('subjects')
    op.drop_table('groups')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('group_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('group_id')
    )
    op.create_table('subjects',
    sa.Column('subject_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('lector_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['lector_id'], ['lectors.lector_id'], ),
    sa.PrimaryKeyConstraint('subject_id')
    )
    op.create_table('lectors',
    sa.Column('lector_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('lector_id')
    )
    op.create_table('grades',
    sa.Column('grade_id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.INTEGER(), nullable=True),
    sa.Column('subject_id', sa.INTEGER(), nullable=True),
    sa.Column('grade', sa.INTEGER(), nullable=True),
    sa.Column('date_received', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.subject_id'], ),
    sa.PrimaryKeyConstraint('grade_id')
    )
    op.create_table('students',
    sa.Column('student_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('group_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.group_id'], ),
    sa.PrimaryKeyConstraint('student_id')
    )
    # ### end Alembic commands ###