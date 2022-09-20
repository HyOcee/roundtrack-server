"""generate all tables

Revision ID: 93cbeeeb7588
Revises: 93914f7e145d
Create Date: 2022-09-11 10:47:36.800669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93cbeeeb7588'
down_revision = '93914f7e145d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('firstName', sa.String(), nullable=False))
    op.add_column('students', sa.Column('lastName', sa.String(), nullable=False))
    op.add_column('students', sa.Column('username', sa.String(), nullable=False))
    op.drop_constraint('students_email_key', 'students', type_='unique')
    op.create_unique_constraint(None, 'students', ['username'])
    op.drop_column('students', 'email')
    op.drop_column('students', 'name')
    op.drop_column('subjects', 'id')
    op.add_column('subjects_offered_by_school', sa.Column('subject_name', sa.String(), nullable=False))
    op.drop_constraint('subjects_offered_by_school_subject_id_fkey', 'subjects_offered_by_school', type_='foreignkey')
    op.create_foreign_key(None, 'subjects_offered_by_school', 'subjects', ['subject_name'], ['name'], ondelete='CASCADE')
    op.drop_column('subjects_offered_by_school', 'subject_id')
    op.add_column('subjects_offered_by_student', sa.Column('subject_name', sa.String(), nullable=False))
    op.drop_constraint('subjects_offered_by_student_subject_id_fkey', 'subjects_offered_by_student', type_='foreignkey')
    op.create_foreign_key(None, 'subjects_offered_by_student', 'subjects', ['subject_name'], ['name'], ondelete='CASCADE')
    op.drop_column('subjects_offered_by_student', 'subject_id')
    op.add_column('subjects_taken_by_teacher', sa.Column('subject_name', sa.String(), nullable=False))
    op.drop_constraint('subjects_taken_by_teacher_subject_id_fkey', 'subjects_taken_by_teacher', type_='foreignkey')
    op.create_foreign_key(None, 'subjects_taken_by_teacher', 'subjects', ['subject_name'], ['name'], ondelete='CASCADE')
    op.drop_column('subjects_taken_by_teacher', 'subject_id')
    op.add_column('teachers', sa.Column('firstName', sa.String(), nullable=False))
    op.add_column('teachers', sa.Column('lastName', sa.String(), nullable=False))
    op.add_column('teachers', sa.Column('username', sa.String(), nullable=False))
    op.drop_constraint('teachers_email_key', 'teachers', type_='unique')
    op.create_unique_constraint(None, 'teachers', ['username'])
    op.drop_column('teachers', 'email')
    op.drop_column('teachers', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teachers', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('teachers', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'teachers', type_='unique')
    op.create_unique_constraint('teachers_email_key', 'teachers', ['email'])
    op.drop_column('teachers', 'username')
    op.drop_column('teachers', 'lastName')
    op.drop_column('teachers', 'firstName')
    op.add_column('subjects_taken_by_teacher', sa.Column('subject_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'subjects_taken_by_teacher', type_='foreignkey')
    op.create_foreign_key('subjects_taken_by_teacher_subject_id_fkey', 'subjects_taken_by_teacher', 'subjects', ['subject_id'], ['id'], ondelete='CASCADE')
    op.drop_column('subjects_taken_by_teacher', 'subject_name')
    op.add_column('subjects_offered_by_student', sa.Column('subject_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'subjects_offered_by_student', type_='foreignkey')
    op.create_foreign_key('subjects_offered_by_student_subject_id_fkey', 'subjects_offered_by_student', 'subjects', ['subject_id'], ['id'], ondelete='CASCADE')
    op.drop_column('subjects_offered_by_student', 'subject_name')
    op.add_column('subjects_offered_by_school', sa.Column('subject_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'subjects_offered_by_school', type_='foreignkey')
    op.create_foreign_key('subjects_offered_by_school_subject_id_fkey', 'subjects_offered_by_school', 'subjects', ['subject_id'], ['id'], ondelete='CASCADE')
    op.drop_column('subjects_offered_by_school', 'subject_name')
    op.add_column('subjects', sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('students', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('students', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'students', type_='unique')
    op.create_unique_constraint('students_email_key', 'students', ['email'])
    op.drop_column('students', 'username')
    op.drop_column('students', 'lastName')
    op.drop_column('students', 'firstName')
    # ### end Alembic commands ###