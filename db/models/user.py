from sqlalchemy import String, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column('username', String(50), primary_key=True)
    password = Column('password', String(50), nullable=False)
    code = Column('code', String(50), nullable=True)
    diffie_hellman_key = Column('diffie_hellman_key', String(50), nullable=True)