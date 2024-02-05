import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import now


class _Base:
    id = sa.Column(sa.BigInteger, primary_key=True, index=True)

    created_at = sa.Column(sa.DateTime, default=now())
    updated_at = sa.Column(sa.DateTime, default=now(), onupdate=now())

    def set_values(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self


Base = declarative_base(cls=_Base)
