import uuid

from tiny.common.models import Base
import sqlalchemy as sa


class ShortCode(Base):
    __tablename__ = "shortcodes"

    url = sa.Column(sa.Text, nullable=False)
    shortcode = sa.Column(sa.Text, nullable=False, unique=True, default=lambda: str(uuid.uuid1()).replace('-', '_'))

    redirect_count = sa.Column(sa.Integer, nullable=False, default=0)
