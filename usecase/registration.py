from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from db.connection import get_session
from db.models import User
from schemas import SignUpRequest

from hashlib import sha256


async def register_user(credentials: SignUpRequest):
    credentials.password = sha256(credentials.password.encode()).hexdigest()
    async with get_session() as session:
        print('12')
        await session.execute(insert(User), [credentials.__dict__])
        await session.commit()



