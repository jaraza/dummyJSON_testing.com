from http import HTTPStatus

import pytest

from conftest import client
from models.dummyJSON_models import UserData
from common_functions.asserts import assert_schema, assert_response_with_file
from common_functions import constants

class TestUserData:
    """
    Тесты получения данных пользователя
    1. test_user_data_success - успешное получение данных пользователя
    2. test_user_data_no_token - попытка получение данных пользователя без токена
    3. test_user_data_wrong_token - попытка получение данных пользователя с неверных токеном  !!!БАГ!!!
    """

    def test_user_data_success(self, client, request):
        """
        успешное получение данных пользователя
        """

        json_data = {'username': constants.LOGIN_ADMIN,
                     'password': constants.PASSWORD_ADMIN}
        response = client.post(constants.EndPoints.LOGIN, data=json_data)
        assert response.status_code == HTTPStatus.OK
        token = response.json()['accessToken']

        headers = {'Authorization': f'Bearer {token}'}
        response = client.get(constants.EndPoints.CURRENT_USER, headers=headers)
        assert response.status_code == HTTPStatus.OK

        # проверка по схеме
        assert_schema(response, UserData)

        # сравнение с эталонным ответом из файла
        assert_response_with_file(response, request, True)


    def test_user_data_no_token(self, client):
        """
        попытка получение данных пользователя без токена
        """

        response = client.get(constants.EndPoints.CURRENT_USER)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        #Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты

    @pytest.mark.xfail(reason="Ссылка на баг")
    def test_user_data_wrong_token(self, client):
        """
        попытка получение данных пользователя с неверным токеном
        """
        json_data = {'username': constants.LOGIN_ADMIN,
                     'password': constants.PASSWORD_ADMIN}
        response = client.post(constants.EndPoints.LOGIN, data=json_data)
        assert response.status_code == HTTPStatus.OK

        token = response.json()['accessToken']
        token = token[:-1]
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get(constants.EndPoints.CURRENT_USER, headers=headers)
        assert response.status_code == HTTPStatus.UNAUTHORIZED #Баг. Падаем, т.к. приходит 500. Ошибка 401 больше подходит

        #Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты