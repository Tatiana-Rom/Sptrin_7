import requests
import allure
import pytest
from data.urls import Urls


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    @allure.description("Создаём нового курьера через API и проверяем ответ")
    def test_create_courier_success(self, generate_courier_data):
        creation_body, _ = generate_courier_data

        with allure.step("Создаём курьера"):
            response = requests.post(Urls.URL_courier_create, json=creation_body)
            assert response.status_code == 201, f"Неверный код: {response.text}"
            assert response.json().get("ok") is True


    @allure.title("Ошибка при создании двух одинаковых курьеров")
    @allure.description("Проверяем, что нельзя создать двух одинаковых курьеров — ответ 409 и сообщение об ошибке")
    def test_create_duplicate_courier(self, created_courier):
        with allure.step("Отправляем повторный запрос на создание курьера"):
            response = requests.post(Urls.URL_courier_create, json=created_courier)

        assert response.status_code == 409 and response.json().get("message") == "Этот логин уже используется"

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @allure.description("Проверяем, что если убрать login или password — ответ 400 и сообщение об ошибке")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, courier_data, missing_field):
        data = courier_data.copy()
        data.pop(missing_field)

        with allure.step(f"Cоздание курьера без поля {missing_field}"):
            response = requests.post(Urls.URL_courier_create, json=data)

        assert response.status_code == 400 and response.json().get("message") == "Недостаточно данных для создания учетной записи"
