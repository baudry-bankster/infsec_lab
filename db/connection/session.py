from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import Settings



class SessionManager:

    def __init__(self) -> None:
        self.refresh()


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance


    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)


    def refresh(self):
        self.engine = create_async_engine(Settings().get_database_url)


def get_session() -> AsyncSession:
    session_maker =  SessionManager().get_session_maker()
    return session_maker()