from http import HTTPStatus

import pytest

from models.dummyJSON_models import CartsData, CartData, CartDeletedData
from common_functions.asserts import assert_schema, assert_response_with_file
from common_functions import constants


class TestCart:
    """
    Тесты корзины
    1. test_get_user_cart_success - успешное получение данных корзин пользователя
    2. test_get_user_cart_wrong_user - попытка обращения к корзине другого пользователя. !!!БАГ!!!
    3. test_get_user_cart_inexistent_user - попытка обращения к корзине несуществующего пользователя
    4. test_get_cart_by_id_success - успешное получение данных корзины по id
    5. test_get_cart_by_id_inexistent_id - попытка обращения к несуществующей корзине
    6. test_get_cart_by_id_unauthorized - попытка обращения к корзине по id без авторизации. !!!БАГ!!!
    7. test_add_cart_success - успешное создание корзины. !!!БАГ НА ТРЕБОВАНИЯ!!!
    8. test_add_cart_empty_body - попытка создания корзины с пустым телом
    9. test_add_cart_wrong_user - попытка создания корзины другому пользователю. !!!БАГ!!!
    10. test_update_cart_success - успешное обновление корзины
    11. test_update_cart_wrong_user - попытка обновление корзины другого пользователя !!!БАГ!!!
    12. test_update_cart_inexistent_cart - попытка обновление несуществующей корзины
    13. test_delete_cart_success - успешное удаление корзины
    14. test_delete_cart_wrong_user - попытка удаления корзины другого пользователя !!!БАГ!!!
    15. test_delete_cart_inexistent_cart - попытка удаления несуществующей корзины
    """


    def test_get_user_cart_success(self, auth_client):
        """
        успешное получение данных корзин пользователя
        """

        #авторизация вынесена в фикстуры, поэтому сразу получаем данные корзин пользователя
        response = auth_client.get(constants.EndPoints.USER_CARTS.format(auth_client.user_id))
        assert response.status_code == HTTPStatus.OK

        # проверка по схеме
        assert_schema(response, CartsData)

        #все данные в корзинах динамические, поэтому проверять их нет особого смысла, лучше проверить
        # при добавлении новой корзины

        #кроме user_id
        assert auth_client.user_id == response.json()["carts"][0]["userId"], \
            "userId корзины не совпадает с id пользователя, для которого эту корзину получали"

    @pytest.mark.xfail(reason="Ссылка на баг")
    def test_get_user_cart_wrong_user(self, auth_client):
        """
        попытка обращения к корзине другого пользователя
        """

        # авторизация вынесена в фикстуры, поэтому сразу получаем данные корзины
        response = auth_client.get(constants.EndPoints.USER_CARTS.format(auth_client.user_id + 1))
        #проверяем что нет доступа к корзине другого пользователя, когда авторизованы под ролью простого пользователя
        assert response.status_code == HTTPStatus.FORBIDDEN
        #Доступ есть, что неправильно. Баг

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты


    def test_get_user_cart_inexistent_user(self, auth_client):
        """
        попытка обращения к корзине несуществующего пользователя
        """

        # авторизация вынесена в фикстуры, поэтому сразу получаем данные корзины
        response = auth_client.get(constants.EndPoints.USER_CARTS.format(7777777777))
        #проверяем что нет доступа к корзине несуществующего пользователя, когда авторизованы под ролью простого
        # пользователя
        assert response.status_code == HTTPStatus.NOT_FOUND

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты


    def test_get_cart_by_id_success(self, auth_client):
        """
        успешное получение данных корзины по id
        """

        #авторизация вынесена в фикстуры, поэтому сразу получаем данные корзин пользователя
        response = auth_client.get(constants.EndPoints.USER_CARTS.format(auth_client.user_id))
        assert response.status_code == HTTPStatus.OK

        # проверка по схеме
        assert_schema(response, CartsData)

        #получаем id первой корзины
        cart_id = response.json()["carts"][0]["id"]

        #получаем данные корзины по id
        response = auth_client.get(constants.EndPoints.CART.format(cart_id))
        assert response.status_code == HTTPStatus.OK

        # проверка по схеме
        assert_schema(response, CartData)

        #все данные в корзине динамические, поэтому проверять их нет особого смысла
        # кроме user_id и id корзины
        response_body = response.json()
        assert auth_client.user_id == response_body.get("userId"), \
            "userId корзины не совпадает с id пользователя, для которого эту корзину получали"
        assert auth_client.user_id == response_body.get("id"), \
            "id корзины не совпадает"


    def test_get_cart_by_id_inexistent_id(self, auth_client):
        """
        попытка обращения к несуществующей корзине
        """

        #авторизация вынесена в фикстуры
        #получаем данные корзины по id
        response = auth_client.get(constants.EndPoints.CART.format(77777777))
        assert response.status_code == HTTPStatus.NOT_FOUND

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты

    @pytest.mark.xfail(reason="Ссылка на баг")
    def test_get_cart_by_id_unauthorized(self, client):
        """
        попытка обращения к корзине без авторизации
        """

        #авторизация вынесена в фикстуры
        #получаем данные корзины по id
        response = client.get(constants.EndPoints.CART.format(1))
        assert response.status_code == HTTPStatus.UNAUTHORIZED #Баг - доступ есть

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты

    def test_add_cart_success(self, auth_client, request):
        """
        успешное создание корзины
        """

        # Авторизация вынесена в фикстуры.
        # Создаем корзину
        json_data = {'userId': auth_client.user_id,
                     'products': [
                         {
                             "id": 144,
                             "quantity": 4,
                         },
                         {
                             "id": 98,
                             "quantity": 1,
                         },
                     ]
                     }
        response = auth_client.post(constants.EndPoints.ADD_CART, json=json_data)
        assert response.status_code == HTTPStatus.CREATED
        # проверяем по схеме
        assert_schema(response, CartData) #Баг на документацию, т.к. products имеет разную структуру в разных ответах
        # сравнение с эталонным ответом из файла
        assert_response_with_file(response, request, True)
        #Удаление созданной корзины не стал дописывать, т.к. по документации самого добавления на сервер не происходит,
        # только симуляция


    def test_add_cart_empty_body(self, auth_client):
        """
        попытка создания корзины с пустым телом
        """

        # Авторизация вынесена в фикстуры.
        # Создаем корзину
        response = auth_client.post(constants.EndPoints.ADD_CART, json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты

    @pytest.mark.xfail(reason="Ссылка на баг")
    def test_add_cart_wrong_user(self, auth_client):
        """
        попытка создания корзины другому пользователю
        """

        # Авторизация вынесена в фикстуры.
        # Создаем корзину
        json_data = {'userId': auth_client.user_id+1,
                     'products': [
                         {
                             "id": 144,
                             "quantity": 4,
                         },
                         {
                             "id": 98,
                             "quantity": 1,
                         },
                     ]
                     }
        response = auth_client.post(constants.EndPoints.ADD_CART, json=json_data)
        print("response: \n", response.json())
        assert response.status_code == HTTPStatus.FORBIDDEN #Баг - козина создается
        
        
    def test_update_cart_success(self, auth_client):
        """
        успешное обновление корзины
        """

        #авторизация вынесена в фикстуры, поэтому сразу получаем данные корзин пользователя
        response = auth_client.get(constants.EndPoints.USER_CARTS.format(auth_client.user_id))
        assert response.status_code == HTTPStatus.OK

        # проверка по схеме
        assert_schema(response, CartsData)
        response_body = response.json()

        #получаем id первой корзины
        cart_id = response_body["carts"][0]["id"]
        old_products_ids = [product["id"] for product in response_body["carts"][0]["products"]]
        old_total_products = response_body["carts"][0]["totalProducts"]
        old_total_quantity = response_body["carts"][0]["totalQuantity"]

        json_data = {'merge': "true",
                     "products": [
                         {
                             "id": 1,
                             "quantity": 1,
                         },
                     ]
                     }
        response = auth_client.put(constants.EndPoints.CART.format(cart_id), json=json_data)
        assert response.status_code == HTTPStatus.OK
        response_body = response.json()

        assert_schema(response, CartData)
        product_ids = [product["id"] for product in response_body["products"]]
        assert product_ids == old_products_ids + [1], "Новый продукт не добавлен в корзину"
        assert response_body["totalProducts"] == old_total_products+1, "Общее количество продуктов не увеличилось"
        assert response_body["totalQuantity"] == old_total_quantity+1, "Общее количество не увеличилось"

    @pytest.mark.xfail(reason="Ссылка на баг")
    def test_update_cart_wrong_user(self, auth_client):
        """
        попытка обновление корзины другого пользователя
        """

        #авторизация вынесена в фикстуры, поэтому сразу получаем данные корзин пользователя
        response = auth_client.get(constants.EndPoints.USER_CARTS.format(auth_client.user_id+1))
        assert response.status_code == HTTPStatus.OK

        # проверка по схеме
        assert_schema(response, CartsData)
        response_body = response.json()

        #получаем id первой корзины
        cart_id = response_body["carts"][0]["id"]

        #добавляем продукт в корзину
        json_data = {'merge': "true",
                     "products": [
                         {
                             "id": 1,
                             "quantity": 1,
                         },
                     ]
                     }
        response = auth_client.put(constants.EndPoints.CART.format(cart_id), json=json_data)
        #проверяем отсутствие доступа к корзине другого пользователя
        assert response.status_code == HTTPStatus.FORBIDDEN #Баг - позволяет обновить корзину другого пользователя

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты

    def test_update_cart_inexistent_cart(self, auth_client):
        """
        попытка обновление несуществующей корзины
        """

        json_data = {'merge': "true",
                     "products": [
                         {
                             "id": 1,
                             "quantity": 1,
                         },
                     ]
                     }
        response = auth_client.put(constants.EndPoints.CART.format(777777777), json=json_data)
        assert response.status_code == HTTPStatus.NOT_FOUND

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты


    def test_delete_cart_success(self, auth_client):
        """
        успешное удаление корзины
        """

        #авторизация вынесена в фикстуры, поэтому сразу получаем данные корзин пользователя
        response = auth_client.get(constants.EndPoints.USER_CARTS.format(auth_client.user_id))
        assert response.status_code == HTTPStatus.OK

        # проверка по схеме
        assert_schema(response, CartsData)

        #получаем id первой корзины
        cart_id = response.json()["carts"][0]["id"]

        response = auth_client.delete(constants.EndPoints.CART.format(cart_id))
        assert response.status_code == HTTPStatus.OK

        #проверяем по схеме удаленной корзины, в том числе, что ответ содержит:
        # "isDeleted": true,
        # "deletedOn": /* ISOTime */
        assert_schema(response, CartDeletedData)

    @pytest.mark.xfail(reason="Ссылка на баг")
    def test_delete_cart_wrong_user(self, auth_client):
        """
        попытка удаления корзины другого пользователя
        """

        #авторизация вынесена в фикстуры, поэтому сразу получаем данные корзин пользователя
        response = auth_client.get(constants.EndPoints.USER_CARTS.format(auth_client.user_id+1))
        assert response.status_code == HTTPStatus.OK

        # проверка по схеме
        assert_schema(response, CartsData)

        #получаем id первой корзины
        cart_id = response.json()["carts"][0]["id"]

        response = auth_client.delete(constants.EndPoints.CART.format(cart_id))
        assert response.status_code == HTTPStatus.FORBIDDEN #Баг - позволяет удалить корзину другого пользователя

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты

    def test_delete_cart_inexistent_cart(self, auth_client):
        """
        попытка удаления несуществующей корзины
        """

        #авторизация вынесена в фикстуры, поэтому сразу получаем данные корзин пользователя

        response = auth_client.delete(constants.EndPoints.CART.format(7777777777))
        assert response.status_code == HTTPStatus.NOT_FOUND

        # Формат ответа нет смысла проверять, т.к. он не указан в документации. По хорошему тут надо идти к аналитикам
        # и дорабатывать документацию, а потом дописывать тесты