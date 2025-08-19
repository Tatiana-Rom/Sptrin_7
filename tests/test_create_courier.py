import allure
import pytest
from client.courier_client import CourierClient
from data.messages import CourierMessages


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    @allure.description("Создаём нового курьера через API и проверяем ответ")
    def test_create_courier_success(self, generate_courier_data):
        creation_body, _ = generate_courier_data

        with allure.step("Создаём курьера"):
            response = CourierClient.create(creation_body)

        assert response.status_code == 201, f"Неверный код: {response.text}"
        assert response.json().get("ok") is True

    @allure.title("Ошибка при создании двух одинаковых курьеров")
    @allure.description("Нельзя создать двух одинаковых курьеров — ответ 409 и сообщение об ошибке")
    def test_create_duplicate_courier(self, generate_courier_data):
        creation_body, _ = generate_courier_data
        CourierClient.create(creation_body)

        with allure.step("Пробуем создать того же курьера ещё раз"):
            response = CourierClient.create(creation_body)

        assert response.status_code == 409
        assert response.json().get("message") == CourierMessages.COURIER_ALREADY_EXISTS

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @allure.description("Если убрать login или password — ответ 400 и сообщение об ошибке")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, generate_courier_data, missing_field):
        creation_body, _ = generate_courier_data
        data = creation_body.copy()
        data.pop(missing_field)

        with allure.step(f"Cоздание курьера без поля {missing_field}"):
            response = CourierClient.create(data)

        assert response.status_code == 400
        assert response.json().get("message") == CourierMessages.NOT_ENOUGH_DATA
