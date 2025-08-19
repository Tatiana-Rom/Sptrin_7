import requests
from data.urls import Urls

class OrderClient:

    @staticmethod
    def get_list():
        return requests.get(Urls.URL_orders_create)

    @staticmethod
    def create(order_data):
        return requests.post(Urls.URL_orders_create, json=order_data)