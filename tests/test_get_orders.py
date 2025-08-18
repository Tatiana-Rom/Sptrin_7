import requests
import allure
import pytest
from data.urls import Urls

class TestOrdersListGet:

    @allure.title("Проверка получения списка заказов")
    @allure.description("Проверка, что список заказов успешно возвращается и имеет корректную структуру.")
    def test_orders_list_get_success(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = requests.get(Urls.URL_orders_create)

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)