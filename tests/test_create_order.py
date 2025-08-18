import requests
import pytest
import allure
from data.urls import Urls
from data.data import OrderData


class TestCreateOrder:

    @allure.title("Создание заказа с разными цветами")
    @allure.description(
        "Проверяется создание заказа с одним цветом, двумя цветами и без указания цвета. "
        "В теле ответа должен быть track."
    )
    @pytest.mark.parametrize("order_data", [
        OrderData.order_black,
        OrderData.order_gray,
        OrderData.order_both,
        OrderData.order_no_color
    ])
    def test_create_order(self, order_data):

        with allure.step(f"Cоздание заказа: {order_data['firstName']}"):
            response = requests.post(Urls.URL_orders_create, json=order_data)

        assert response.status_code == 201 and "track" in response.json()
