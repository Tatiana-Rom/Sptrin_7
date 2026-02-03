import pytest
from client.courier_client import CourierClient
from helpers import create_random_login, create_random_password, create_random_firstname


@pytest.fixture
def generate_courier_data():
    login = create_random_login()
    password = create_random_password()
    first_name = create_random_firstname()

    creation_body = {"login": login, "password": password, "firstName": first_name}
    login_body = {"login": login, "password": password}

    yield creation_body, login_body

    login_response = CourierClient.login(login_body)
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        CourierClient.delete(courier_id)
