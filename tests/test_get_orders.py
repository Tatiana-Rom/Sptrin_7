import pytest
import allure
from client.order_client import OrderClient


class TestOrdersListGet:

    @allure.title("Проверка получения списка заказов")
    @allure.description("Проверка, что список заказов успешно возвращается и имеет корректную структуру.")
    def test_orders_list_get_success(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = OrderClient.get_list()

        assert response.status_code == 200
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list), "Список заказов должен быть массивом"