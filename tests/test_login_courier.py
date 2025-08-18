import pytest
import requests
import allure
from data.urls import Urls


class TestCourierLogin:

    @allure.title("Проверка успешной аутентификации курьера при вводе валидных данных")
    def test_login_success(self, generate_courier_data):
        creation_body, login_body = generate_courier_data
        requests.post(Urls.URL_courier_create, json=creation_body)

        with allure.step("Авторизация курьером"):
            response = requests.post(Urls.URL_courier_login, json=login_body)
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Проверка получения ошибки аутентификации курьера при вводе невалидных данны")
    @pytest.mark.parametrize("wrong_data", [
        {"login": "wrong", "password": "valid_pass"},
        {"login": "valid_login", "password": "wrong"},
    ])
    def test_login_wrong_credentials(self, wrong_data, generate_courier_data):
        creation_body, login_body = generate_courier_data
        requests.post(Urls.URL_courier_create, json=creation_body)

        wrong_data = {
            "login": wrong_data["login"].replace("valid_login", login_body["login"]),
            "password": wrong_data["password"].replace("valid_pass", login_body["password"]),
        }

        with allure.step("Логинимся с невалидными данными"):
            response = requests.post(Urls.URL_courier_login, json=wrong_data)
            assert response.status_code == 404 and response.json().get("message") == "Учетная запись не найдена"

    @allure.title("Проверка получения ошибки аутентификации курьера с пустым полем логина или пароля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field, generate_courier_data):
        creation_body, login_body = generate_courier_data
        requests.post(Urls.URL_courier_create, json=creation_body)

        login_payload = login_body.copy()
        login_payload.pop(missing_field)

        with allure.step(f"Авторизация без поля {missing_field}"):
            response = requests.post(Urls.URL_courier_login, json=login_payload)
            assert response.status_code == 400 and response.json().get("message") == "Недостаточно данных для входа"

    @allure.title("Авторизация под несуществующим пользователем возвращает ошибку")
    def test_login_nonexistent_user(self, nonexistent_courier_data):
        with allure.step("Авторизация под несуществующим пользователем"):
            response = requests.post(Urls.URL_courier_login, json=nonexistent_courier_data)
            assert response.status_code == 404 and response.json().get("message") == "Учетная запись не найдена"
