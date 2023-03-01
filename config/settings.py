from pydantic import BaseSettings
from os import environ


class Settings(BaseSettings):

    POSTGRES_HOST = environ.get('POSTGRES_HOST', '127.0.0.1')
    POSTGRES_USER = environ.get('POSTGRES_USER', 'site')
    POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD', 'site')
    POSTGRES_PORT = environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DB = environ.get('POSTGRES_DB', 'site')
    
    # POSTGRES_ = environ.get('POSTGRES_', )
    # POSTGRES_ = environ.get('POSTGRES_', )


    @property
    def get_database_url(self) -> str:
        print(f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost/{self.POSTGRES_DB}')
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost/{self.POSTGRES_DB}'



    class Config:

        env_file = '.env'
        env_file_encoding = 'utf-8'