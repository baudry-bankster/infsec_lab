from fastapi import FastAPI, status, Depends, Response
from fastapi.responses import JSONResponse

from usecase import register_user, get_code, auth_by_code
from schemas.signUp import SignUpRequest
from schemas.signIn import SignInRequest, CodeResponse, CodeRequest
from exceptions import *


app = FastAPI()



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