from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

import settings


metadata = MetaData()

Users_tab = Table('Users_tab', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('email', String, unique=True, nullable=False)
                  )

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
