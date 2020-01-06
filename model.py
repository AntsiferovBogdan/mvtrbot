from sqlalchemy import *

md = MetaData()

Users_tab = Table('Users_tab', md,
                  Column('id', Integer, primary_key=True),
                  Column('user', String, nullable=False),
                  Column('email', String, unique=True, nullable=False)
                  )
