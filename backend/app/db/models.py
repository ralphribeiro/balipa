from sqlalchemy import Boolean, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import backref, relationship

from .session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


class Local(Base):
    __tablename__ = "local"

    id = Column(Integer, primary_key=True, index=True)
    volume = Column(Integer)
    coordinate = Column(String, nullable=False)

    items = relationship("Item", back_populates="locale")


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    volume = Column(Integer, nullable=False)
    price = Column(Numeric)
    local_id = Column(Integer, ForeignKey('local.id'))

    locale = relationship("Local", back_populates="items")
