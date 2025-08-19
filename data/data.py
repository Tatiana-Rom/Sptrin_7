class Data:
    valid_login = 'AmiTyan'
    valid_password = '123123'
    valid_firstname = 'Ami'
    valid_courier_data = {'login': 'AmiTyan', 'password': '123123', 'firstName': 'Ami'}
    courier_data_without_name = {'login': 'AmiTyan', 'password': '123123'}
    courier_data_with_wrong_password = {'login': 'AmiTyan', 'password': '123456'}

class OrderData:
    order_base = {
        "firstName": "Ami",
        "lastName": "Tyan",
        "address": "Moscow, 13 apt.",
        "metroStation": 5,
        "phone": "+7 897 123 45 56",
        "rentTime": 5,
        "deliveryDate": "2025-08-16",
        "comment": "As fast as you can"
    }

    order_black = {**order_base, "color": ["BLACK"]}
    order_gray = {**order_base, "color": ["GREY"]}
    order_both = {**order_base, "color": ["BLACK", "GREY"]}
    order_no_color = {**order_base}

class CourierData:

    nonexistent = {
        "login": "nonexistent_user",
        "password": "nopass"
    }

class WrongCourierData:
    wrong_login = {"login": "wrong", "password": None}
    wrong_password = {"login": None, "password": "wrong"}