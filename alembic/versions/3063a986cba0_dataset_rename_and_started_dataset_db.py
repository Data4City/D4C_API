"""Dataset rename, and started dataset db

Revision ID: 3063a986cba0
Revises: 6b499b7fc09f
Create Date: 2019-10-01 12:02:51.532925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3063a986cba0'
down_revision = '6b499b7fc09f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dbfile', sa.Column('label', sa.Enum('air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 'drilling', 'engine_idling', 'gun_shot', 'jackhammer', 'siren', 'street_music', name='labelsenum'), nullable=True))
    op.add_column('inference', sa.Column('predicted_label', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'inference', 'labels', ['predicted_label'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'inference', type_='foreignkey')
    op.drop_column('inference', 'predicted_label')
    op.drop_column('dbfile', 'label')

    # ### end Alembic commands ###
