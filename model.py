from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    user_email = Column(Integer, unique=True)


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()
