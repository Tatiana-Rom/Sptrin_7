import pytest
import requests
import random
import string
from data.urls import Urls
from helpers import create_random_login, create_random_password, create_random_firstname

def generate_random_courier_data():
    def random_string(length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    return {
        "login": "courier_" + random_string(10),
        "password": random_string(10),
        "firstName": random_string(10).capitalize()
    }

@pytest.fixture
def courier_data():
    return generate_random_courier_data()

@pytest.fixture
def created_courier(courier_data):
    response = requests.post(Urls.URL_courier_create, data=courier_data)
    assert response.status_code in [201, 409]
    yield courier_data

    login_data = {
        "login": courier_data["login"],
        "password": courier_data["password"]
    }
    login_response = requests.post(Urls.URL_courier_login, data=login_data)
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        requests.delete(f'{Urls.URL_courier_create}{courier_id}')

@pytest.fixture
def generate_courier_data():
    login = create_random_login()
    password = create_random_password()
    first_name = create_random_firstname()

    creation_body = {"login": login, "password": password, "firstName": first_name}
    login_body = {"login": login, "password": password}

    yield creation_body, login_body

    login_response = requests.post(Urls.URL_courier_login, json=login_body)
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        requests.delete(f"{Urls.URL_courier_create}/{courier_id}")

@pytest.fixture
def nonexistent_courier_data():
    return {"login": "nonexistent_user", "password": "nopass"}