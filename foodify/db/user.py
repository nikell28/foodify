from sqlalchemy import Boolean, Column, String

from foodify.db.base import Base


class User(Base):
    tg_id = Column(String, unique=True, nullable=False)
    tg_username = Column(String, nullable=True)
    tg_first_name = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True, default=False)
