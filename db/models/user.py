from sqlalchemy import String, Integer, Column, Table, MetaData


metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('username', String(30), primary_key=True),
    Column('password', String(70), nullable=False),
    Column('code_word', String(70), nullable=True)
)