from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from db.models import User
from db.connection import get_session
from tools.code import get_random_code_word
from exceptions import UserNotFound
from hashlib import sha256

async def get_code(username: str) -> str:
    try:
        async with get_session() as session:
            code = sha256((get_random_code_word().encode())).hexdigest()
            query = (update(User).where(User.username == username).values(code = code))
            await session.execute(query)
            await session.commit()
            return code
    except (IntegrityError, NoResultFound):
        raise UserNotFound


