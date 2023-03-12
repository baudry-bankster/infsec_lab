from fastapi import FastAPI, status, Depends, Response, Header
from fastapi.responses import JSONResponse
from random import randint

from usecase import register_user, get_code, auth_by_code
from schemas.signUp import SignUpRequest
from schemas.signIn import SignInRequest, CodeResponse, CodeRequest
from exceptions import *
from tools.diffie_hellman import get_primitive_root, get_safe_prime, fast_pow
from tools.rc4 import encrypt


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
        return JSONResponse({'message': str(err)}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse({'code': code}, status_code=status.HTTP_200_OK)



@app.get('/get_diffie_params',
         status_code=status.HTTP_200_OK,
         response_class=Response)
async def get_A(bit: int, username: str):
        p = get_safe_prime(bit)
        g = get_primitive_root(bit, p)
        a = randint(10000, 10000)
        A = fast_pow(g, a, p)
        # print(f'Created: p:{p} a:{a} g:{g} for user {username}')
        DATABASE_IN[username] = {'p': p, 'A': A, 'g': g, 'a': a}
        return JSONResponse({'p': p, 'A': A, 'g': g}, status_code=status.HTTP_200_OK)


@app.get('/get_user_param_diffie_hellman',
         status_code=status.HTTP_200_OK,
         response_class=Response)
async def get_K(B: int, username: str):
        data = DATABASE_IN[username]
        k = fast_pow(B, data['a'], data['p'])
        # print(f'Server key = {k} for username {username}')
        DATABASE_IN[username]['k'] = k


@app.get('/send_secret_text',
         status_code=status.HTTP_200_OK,
         response_class=Response
            )
async def send_message(username: str, enc_message: str):
      text = encrypt(enc_message, DATABASE_IN[username]['k'])
    #   answer = 'Server got text enc {}'.format(enc_message)
    #   print(answer)
      answer = 'Server got text {}'.format(text)
    #   print(answer)
      return JSONResponse({'text': encrypt(answer, DATABASE_IN[username]['k'])}, status_code=status.HTTP_200_OK)
