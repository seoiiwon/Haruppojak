"""empty message

Revision ID: 1f59b60711b6
Revises: 
Create Date: 2024-08-03 19:03:50.005846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f59b60711b6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('challenge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('challengeOwner', sa.String(), nullable=False),
    sa.Column('challengeTitle', sa.String(), nullable=False),
    sa.Column('challengeComment', sa.Text(), nullable=False),
    sa.Column('challenger', sa.Integer(), nullable=False),
    sa.Column('challengeReward', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('challengeThumbnail1', sa.String(), nullable=False),
    sa.Column('challengeThumbnail2', sa.String(), nullable=True),
    sa.Column('challengeThumbnail3', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proofShot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userID', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('photoComment', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userdiary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Date', sa.DateTime(), nullable=False),
    sa.Column('Diarycontent', sa.Text(), nullable=False),
    sa.Column('Response', sa.Text(), nullable=False),
    sa.Column('Diarytodo', sa.String(), nullable=True),
    sa.Column('Diaryuserid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userinfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userID', sa.String(), nullable=False),
    sa.Column('userPassword', sa.String(), nullable=False),
    sa.Column('userName', sa.String(length=25), nullable=False),
    sa.Column('userBirth', sa.Integer(), nullable=False),
    sa.Column('userEmail', sa.String(length=255), nullable=False),
    sa.Column('userGender', sa.Integer(), nullable=False),
    sa.Column('userPpojakCoin', sa.Integer(), nullable=False),
    sa.Column('userProfileName', sa.String(), nullable=False),
    sa.Column('userProfileComment', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('role', sa.Enum('ADMIN', 'EDITOR', 'READER', name='userrole'), nullable=True),
    sa.Column('follower', sa.Integer(), nullable=True),
    sa.Column('following', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('userEmail'),
    sa.UniqueConstraint('userID'),
    sa.UniqueConstraint('userName')
    )
    op.create_table('todolist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('todo', sa.String(), nullable=False),
    sa.Column('check', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['userinfo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todolist_id'), 'todolist', ['id'], unique=False)
    op.create_table('userChallenge',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('challenge_id', sa.Integer(), nullable=False),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenge.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['userinfo.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'challenge_id')
    )
    op.create_table('userProofShot',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('photo_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['photo_id'], ['proofShot.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['userinfo.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'photo_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userProofShot')
    op.drop_table('userChallenge')
    op.drop_index(op.f('ix_todolist_id'), table_name='todolist')
    op.drop_table('todolist')
    op.drop_table('userinfo')
    op.drop_table('userdiary')
    op.drop_table('proofShot')
    op.drop_table('challenge')
    # ### end Alembic commands ###
