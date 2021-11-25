from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User get info cases")
class TestUserGet(BaseCase):

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test trying to get user info without login")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("This test successfully get user info with the same user")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test trying to get info user that is not same than authorize user")
    def test_get_user_details_from_other_user(self):
        # REGISTER USER 1
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        first_user_id = self.get_json_value(response1, "id")

        # REGISTER USER 2
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email = register_data["email"]
        password = register_data["password"]

        # LOGIN USER 2
        login_data = {
            "email": email,
            "password": password
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # GET USER 1 DETAILS FROM USER 2
        response4 = MyRequests.get(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response4, "username")
        Assertions.assert_json_has_no_key(response4, "email")
        Assertions.assert_json_has_no_key(response4, "firstName")
        Assertions.assert_json_has_no_key(response4, "lastName")


