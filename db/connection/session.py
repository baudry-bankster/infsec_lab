from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from config import Settings



class SessionManager:

    def __init__(self) -> None:
        self.refresh()


    def __new__(cls):
        if hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncEngine, expire_on_commit=False)


    def refresh(self):
        self.engine = create_async_engine(Settings.get_database_url)


def get_session():
    return SessionManager.get_session_maker()