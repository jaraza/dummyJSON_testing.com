from enum import Enum

LOGIN_ADMIN = "emilys"
PASSWORD_ADMIN = "emilyspass"
LOGIN_USER = "madisonc"
PASSWORD_USER = "madisoncpass"

class EndPoints(str, Enum):
    LOGIN = '/auth/login'
    CURRENT_USER = '/auth/me'
    REFRESH_SESSION = '/auth/refresh'
    CARTS = '/carts'
    CART = '/carts/{}'
    USER_CARTS = '/carts/user/{}'
    ADD_CART = '/carts/add'

    def __str__(self) -> str:
        return self.value

