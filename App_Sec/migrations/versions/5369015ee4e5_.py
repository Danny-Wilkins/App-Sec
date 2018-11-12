"""empty message

Revision ID: 5369015ee4e5
Revises: 83d69b846870
Create Date: 2018-11-11 03:08:43.799017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5369015ee4e5'
down_revision = '83d69b846870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('url', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_image_url'), 'image', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_image_url'), table_name='image')
    op.drop_column('image', 'url')
    # ### end Alembic commands ###