from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User delete cases")
class TestUserDelete(BaseCase):

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test is trying to delete user with id 2")
    def test_delete_user_with_id_2(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        user_id = 2

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # DELETE

        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )
        Assertions.assert_code_status(response2, 400)
        assert response2.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected response {response2.text}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("This test successfully delete user")
    def test_user_delete(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": email, "password": password}
        )
        Assertions.assert_code_status(response3, 200)
        response4 = MyRequests.get(f"/user/{user_id}")
        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found", f"User with email {email} wasn't delete correctly"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("This test trying to delete user that is not same than authorize user")
    def test_delete_user_authorize_other_user(self):
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

        # DELETE
        response4 = MyRequests.delete(
            f"/user/{first_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response4, 400)
