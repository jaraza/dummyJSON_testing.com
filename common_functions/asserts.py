import json

from typing import Type
from pydantic import BaseModel
from common_functions.json import remove_dynamic_data

def assert_schema(response, model: Type[BaseModel]):
    """
    проверяет тело ответа на соответствие его схеме механизмами pydantic
    :param response: ответ от сервера
    :param model: модель, по которой будет проверяться схема json
    :raises ValidationError: если тело ответа не соответствует схеме
    """
    body = response.json()
    if isinstance(body, list):
        for item in body:
            model.model_validate(item, strict=True)
    else:
        model.model_validate(body, strict=True)


def assert_response_with_file(response, path, no_dynamic_data=False):
    """
    проверяет тело ответа на соответствие его эталонному ответу из файла
    :param response: ответ от сервера
    :param path: путь к файлу, с которым будет выполняться сравнение json
    :param no_dynamic_data: пропустить проверку динамических данных - ids и tokens
    :raises ValidationError: если тело ответа не соответствует схеме
    """
    response_body = response.json()
    #при необходимости убирает динамические данные из ответа
    if no_dynamic_data:
        response_body = remove_dynamic_data(response_body)

    #открываем эталонный файл по пути "test_data/{имя теста}.json"
    with open(f"test_data/{path.node.originalname}.json", "r") as f:
        file_data = json.load(f)

    assert response_body == file_data, "Тело ответа не совпадает с эталоном"