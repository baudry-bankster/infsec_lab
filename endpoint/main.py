from usecase.registration import register_user
from fastapi import FastAPI
from schemas.signUp import SignUpRequest



app = FastAPI()



@app.post('/register')
async def signup(credentials: SignUpRequest):
    # try:
    await register_user(credentials=credentials)
    # except:
    #     print('Error register user')