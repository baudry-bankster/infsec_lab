class UserExists(Exception):
    def __str__(self):
        return "User with current username already exists"


class UserNotFound(Exception):
    def __str__(self):
        return "User with current username not found"


class InvalidCredentials(Exception):
    def __str__(self):
        return "Invalid password"