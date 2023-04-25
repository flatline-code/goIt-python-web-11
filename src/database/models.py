from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String(50), nullable=True)
    birthday = Column('birthday', Date, nullable=False)
    description = Column(String(150), nullable=False)
