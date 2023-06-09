from sqlalchemy import Column, String

from foodify.db.base import Base


class User(Base):
    tg_id = Column(String, unique=True, nullable=False)
    tg_username = Column(String, nullable=True)
    tg_first_name = Column(String, nullable=True)
