from faker import Faker

faker = Faker('ru_RU')

def create_random_login():
    login = faker.text(max_nb_chars=7) + str(faker.random_int(0, 999))
    return login

def create_random_password():
    password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return password

def create_random_firstname():
    first_name = faker.first_name()
    return first_name

