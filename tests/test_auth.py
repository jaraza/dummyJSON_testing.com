from http import HTTPStatus

from models.dummyJSON_models import LoginData
from common_functions.asserts import assert_schema, assert_response_with_file
from common_functions import constants


class TestAuth:
    """
    Тесты авторизации
    1. test_auth_success - успешная авторизация
    2. test_auth_wrong_password - попытка авторизации с неверным паролем
    3. test_auth_empty_body - попытка авторизации с пустым телом запроса
    """

    def test_auth_success(self, client, request):
        """
        Успешная авторизация
        """
        json_data =  {'username': constants.LOGIN_ADMIN,
                      'password': constants.PASSWORD_ADMIN}
        response = client.post(constants.EndPoints.LOGIN, data= json_data)
        assert response.status_code == HTTPStatus.OK
        #проверка по схеме
        assert_schema(response, LoginData)

        #сравнение с эталонным ответом из файла
        assert_response_with_file(response, request, True)


    def test_auth_wrong_password(self, client):
        """
        попытка авторизации с неверным паролем
        """
        json_data =  {'username': constants.LOGIN_ADMIN,
                      'password': '12345'}
        response = client.post(constants.EndPoints.LOGIN, data= json_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        #Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты


    def test_auth_empty_body(self, client):
        """
        попытка авторизации с пустым телом запроса
        """
        json_data =  {}
        response = client.post(constants.EndPoints.LOGIN, data= json_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        #Формат ответа нет смысла проверять, т.к. он не указан в документации

