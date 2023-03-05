from random import choice


chars = list('qwertyuiopasdfghjklzxcvbnm,.!@#$%^&*()1234567890')


def get_random_code_word() -> str:
    return ''.join([choice(chars) for i in range(25)])