import os
import pytest
import requests


from dotenv import load_dotenv
from common_functions import constants
from http import HTTPStatus

pytest.register_assert_rewrite("common_functions.asserts")

class ApiSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.base_url = f"https://{os.getenv('RESOURCE_URL')}"

    def request(self, method, url, *args, **kwargs):
        if url.startswith("/"):
            url = f"{self.base_url}{url}"
        return super().request(method, url, *args, **kwargs)

class AuthApiSession(ApiSession):
    def __init__(self):
        super().__init__()
        #авторизация
        json_data = {'username': constants.LOGIN_USER,
                     'password': constants.PASSWORD_USER}
        response = self.post(constants.EndPoints.LOGIN, data=json_data)
        assert response.status_code == HTTPStatus.OK
        token = response.json()['accessToken']
        self.headers['Authorization'] = f'Bearer {token}'
        #сохранение id пользователя
        self.user_id = response.json()['id']

def pytest_configure(config):
    # устанавливаем текущую директорию на корень проекта (это позволит прописывать относительные пути к файлам)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # загружаем переменные-параметры из файла /.env
    load_dotenv(dotenv_path=".env")

@pytest.fixture
def client():
    return ApiSession()

@pytest.fixture
def auth_client():
    return AuthApiSession()