import json
from datetime import datetime
from requests import Response
import string
import random


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response test is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None, username_len: int = None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        current_username = "learnqa"
        if username_len is not None:
            current_username = "".join(random.choice(string.ascii_lowercase) for i in range(username_len))
        return {
            "password": "123",
            "username": current_username,
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }
