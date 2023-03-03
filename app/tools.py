import requests
from hashlib import sha256
from tkinter.messagebox import showinfo
from exceptions import UserExists

def registration(username: str, password: str):
    result = requests.post('http://127.0.0.1:8000/signup', data={'username': username, 'password': password})
    status = str(result.status_code)
    if status in ['409']:
        showinfo('info', result.json()['message'])
        print(result.json()['message'])
        return ValueError(result.json()['message'])
    if status in ['422']:
        showinfo('info', result.json()['detail'][0]['msg'])
        print(result.json()['detail'][0]['msg'])
        return ValueError(result.json()['detail'][0]['msg'])
    else:
        showinfo('info', 'Registration is completed')
        print('Registration: {} , {}'.format(username, password))


def get_code(username: str) -> str:
    result = requests.post('http://127.0.0.1:8000/auth_code', json={'username': username})
    # print('get by code for  {}'.format(username))
    status = str(result.status_code)
    if status in ['404']:
        showinfo('info', result.json()['message'])
        print(result.json()['message'])
        return ValueError(result.json()['message'])
    if status in ['422']:
        showinfo('info', result.json()['detail'][0]['msg'])
        print(result.json()['detail'][0]['msg'])
        return ValueError(result.json()['detail'][0]['msg'])
    else:
        print('Code has been received')
        return result.json()['code']


def auth(username: str, code: str, password: str):
    hash_password = sha256((str(sha256(password.encode()).hexdigest()) + code).encode()).hexdigest()
    result = requests.post('http://127.0.0.1:8000/signin', json={'username': username, 'hash_password': hash_password})
    print('code: {}'.format(code))
    print('hash_password: {}'.format(str(sha256(password.encode()).hexdigest())))
    print('hash_password + code: {}'.format(hash_password))
    status = str(result.status_code)
    if status in ['404', '401']:
        showinfo('info', result.json()['message'])
        print(result.json()['message'])
        return ValueError(result.json()['message'])
    if status in ['422']:
        showinfo('info', result.json()['detail'][0]['msg'])
        print(result.json()['detail'][0]['msg'])
        return ValueError(result.json()['detail'][0]['msg'])
    else:
        print('User has been authenticated')
        showinfo('info', 'User has been authenticated')


def full_auth(username: str, password: str):
    try:
        code = get_code(username)
        auth(username, code, password)
    except:
        showinfo('info', 'Error!\nRepeat again')