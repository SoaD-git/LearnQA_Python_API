import random
from datetime import datetime
import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User register cases")
class TestUserRegister(BaseCase):

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("This test successfully create user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test trying to create user with existing email")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test trying to create user with email without @")
    def test_create_user_with_email_without_at(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format",\
            f"Invalide email '{email}' is valid"

    exclude_params = [("username"), ("firstName"), ("lastName"), ("email"), ("password")]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test trying to create user without one of required params field")
    @pytest.mark.parametrize("condition", exclude_params)
    def test_create_user_without_some_user_params(self, condition):

        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        if condition == "username":
            data = {
                "password": "123",
                "firstName": "learnqa",
                "lastName": "learnqa",
                "email": email
            }
        elif condition == "firstName":
            data = {
                "password": "123",
                "username": "learnqa",
                "lastName": "learnqa",
                "email": email
            }
        elif condition == "lastName":
            data = {
                "password": "123",
                "username": "learnqa",
                "firstName": "learnqa",
                "email": email
            }
        elif condition == "email":
            data = {
                "password": "123",
                "username": "learnqa",
                "firstName": "learnqa",
                "lastName": "learnqa",
            }
        elif condition == "password":
            data = {
                "username": "learnqa",
                "firstName": "learnqa",
                "lastName": "learnqa",
                "email": email
            }
        else:
            data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}",\
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test trying to create user with username length 1 symbol")
    def test_create_user_with_one_symbol(self):
        data = self.prepare_registration_data(username_len=1)

        response = MyRequests.post("/user/", data=data)
        print(response.content, response.status_code)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test trying to create user with username length from 251 to 500 symbols")
    def test_create_user_with_over_250_symbols(self):
        data = self.prepare_registration_data(username_len=random.randrange(251, 500))

        response = MyRequests.post("/user/", data=data)
        print(response.content, response.status_code)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long", \
            f"Unexpected response content {response.content}"
