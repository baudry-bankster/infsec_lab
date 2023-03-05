from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from hashlib import sha256

from db.models import User
from schemas.signIn import SignInRequest
from db.connection import get_session
from exceptions import UserNotFound, InvalidCredentials


async def __get_user_credentials(credentials: SignInRequest):
    try:
        async with get_session() as session:
            query = (select(User.password, User.code).where(User.username==credentials.username))
            result = await session.execute(query)
            return result.one()
    except (IntegrityError, NoResultFound):
        raise UserNotFound
    


async def auth_by_code(credentials: SignInRequest):
    hash_password, code = await __get_user_credentials(credentials)
    print('code: {}\nhash _password: {} '.format(code, hash_password))
    print('hash_password + code: {}'.format(sha256((hash_password + code).encode()).hexdigest()))
    if credentials.hash_password != sha256((hash_password + code).encode()).hexdigest():
        raise InvalidCredentials