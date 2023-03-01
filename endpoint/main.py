from fastapi import FastAPI, status, Depends, Response, Header
from fastapi.responses import JSONResponse
from random import randint

from usecase import register_user, get_code, auth_by_code
from schemas.signUp import SignUpRequest
from schemas.signIn import SignInRequest, CodeResponse, CodeRequest
from exceptions import *
from tools.diffie_hellman import get_primitive_root, get_safe_prime, fast_pow


app = FastAPI()

DATABASE_IN = {}


@app.post(
        '/signup',
        status_code=status.HTTP_201_CREATED,    
        response_class=Response,)
async def signup(credentials: SignUpRequest = Depends(SignUpRequest.as_form)):
    try:
        await register_user(credentials=credentials)
    except UserExists as err:
        return JSONResponse({'message': str(err)}, status_code=status.HTTP_409_CONFLICT)


@app.post('/signin',
          response_class=Response,
          status_code=status.HTTP_202_ACCEPTED)
async def signin(credentials: SignInRequest):
    try:
        await auth_by_code(credentials)
    except InvalidCredentials as err:
        return JSONResponse({'message': str(err)}, status_code=status.HTTP_404_NOT_FOUND)
    except UserNotFound as err:
        return JSONResponse({'message': str(err)}, status_code=status.HTTP_401_UNAUTHORIZED)
        


@app.post('/auth_code',
          status_code=status.HTTP_200_OK,
          response_model=CodeResponse)
async def signin(credentials: CodeRequest):
    try:
        code = await get_code(credentials.username)
    except UserNotFound as err:
        return JSONResponse({'message': str(err)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({'code': code}, status_code=status.HTTP_200_OK)



@app.get('/get_diffie_params',
         status_code=status.HTTP_200_OK,
         response_class=Response)
async def get_A(bit: int, user: str):
        p = get_safe_prime(70)
        g = get_primitive_root(70, p)
        a = randint(10000, 10000)
        A = fast_pow(g, a, p)
        print(f'Created: p:{p} a:{a} g:{g}')
        DATABASE_IN[user] = {'p': p, 'A': A, 'g': g, 'a': a}
        return JSONResponse({'p': p, 'A': A, 'g': g}, status_code=status.HTTP_200_OK)


@app.get('/get_user_param_diffie_hellman',
         status_code=status.HTTP_200_OK,
         response_class=Response)
async def get_A(B: int, user: str):
        data = DATABASE_IN[user]
        k = fast_pow(B, data['a'], data['p'])
        print(f'Server key = {k}')
        DATABASE_IN[user]['k'] = k