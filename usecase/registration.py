from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from db.connection import get_session
from db.models import User
from schemas import SignUpRequest

from hashlib import sha256

from exceptions import UserExists


async def register_user(credentials: SignUpRequest):
    credentials.password = sha256(credentials.password.encode()).hexdigest()
    try:
        async with get_session() as session:
            await session.execute(insert(User), [credentials.__dict__])
            await session.commit()
    except IntegrityError:
        raise UserExists



