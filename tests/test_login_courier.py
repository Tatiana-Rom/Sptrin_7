import pytest
import requests
import allure
from data.urls import Urls
from data.data import WrongCourierData
from data.data import CourierData
from data.messages import LoginMessages


class TestCourierLogin:

    @allure.title("Проверка успешной аутентификации курьера при вводе валидных данных")
    def test_login_success(self, generate_courier_data):
        creation_body, login_body = generate_courier_data
        requests.post(Urls.URL_courier_create, json=creation_body)

        with allure.step("Авторизация курьером"):
            response = requests.post(Urls.URL_courier_login, json=login_body)
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Ошибка аутентификации курьера при вводе невалидных данных")
    @pytest.mark.parametrize("wrong_data", [
        WrongCourierData.wrong_login,
        WrongCourierData.wrong_password,
    ])
    def test_login_wrong_credentials(self, wrong_data, generate_courier_data):
        creation_body, login_body = generate_courier_data
        requests.post(Urls.URL_courier_create, json=creation_body)

        login_payload = {
            "login": wrong_data["login"] or login_body["login"],
            "password": wrong_data["password"] or login_body["password"],
        }

        with allure.step("Логинимся с невалидными данными"):
            response = requests.post(Urls.URL_courier_login, json=login_payload)
            assert response.status_code == 404
            assert response.json().get("message") == LoginMessages.COURIER_NOT_FOUND

    @allure.title("Ошибка аутентификации курьера с пустым полем логина или пароля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field, generate_courier_data):
        creation_body, login_body = generate_courier_data
        requests.post(Urls.URL_courier_create, json=creation_body)

        login_payload = login_body.copy()
        login_payload.pop(missing_field)

        with allure.step(f"Авторизация без поля {missing_field}"):
            response = requests.post(Urls.URL_courier_login, json=login_payload)
            assert response.status_code == 400
            assert response.json().get("message") == LoginMessages.NOT_ENOUGH_DATA

    @allure.title("Авторизация под несуществующим пользователем возвращает ошибку")
    def test_login_nonexistent_user(self):
        with allure.step("Авторизация под несуществующим пользователем"):
            response = requests.post(Urls.URL_courier_login, json=CourierData.nonexistent)
        assert response.status_code == 404
        assert response.json().get("message") == LoginMessages.COURIER_NOT_FOUND
