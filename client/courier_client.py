import requests
from data.urls import Urls

class CourierClient:
    @staticmethod
    def create(courier_data):
        return requests.post(Urls.URL_courier_create, json=courier_data)

    @staticmethod
    def login(login_data):
        return requests.post(Urls.URL_courier_login, json=login_data)

    @staticmethod
    def delete(courier_id):
        return requests.delete(f"{Urls.URL_courier_create}/{courier_id}")