from sqlalchemy import Column, Integer, String
from db import Base, engine

class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(32))
    email = Column('email', String, unique=True, index=True)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
