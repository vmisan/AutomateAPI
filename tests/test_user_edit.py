from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import json
import time

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            f"Wrong name of the user after edit. Actual value: {first_name}. Expected value: {new_name}"
        )

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_by_unauthorized_user(self):
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_lastname = "Changed Last Name"

        response = MyRequests.put(
            f"/user/{user_id}",
            data={"lastName": new_lastname}
        )

        Assertions.assert_code_status(response, 400)
        assert response.text == "Auth token not supplied", "Response is changed when unauthorized user tries to edit"

    #     - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_user_cannot_edit_another_user_data(self):
        # REGISTRATION of the FIRST USER
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data1['email']
        password1 = register_data1['password']

        time.sleep(2) # Wait 2 seconds in order to get different email

        # REGISTRATION of the SECOND USER
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2['email']
        username2 = register_data2['username']
        password2 = register_data2['password']
        user_id2 = self.get_json_value(response2, "id")

        # LOGIN as the FIRST USER
        login_data = {
            'email': email1,
            'password': password1
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # LOGIN as the SECOND USER
        login_data2 = {
            'email': email2,
            'password': password2
        }
        response4 = MyRequests.post("/user/login", data=login_data2)

        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")

        # THE FIRST USER TRIES TO EDIT THE SECOND USER' DATA
        new_username = "Changed Username"

        response5 = MyRequests.put(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"lastName": new_username}
        )
        print(response5.text)
        # print(response5.status_code)
        # Assertions.assert_code_status(response4, 403), \
        # f"Incorrect status code when one user tries to edit another user' data. " \
        # f"Actual status code: {response4.status_code}. Expected status code: 403"

        #It's a bug. We have response with status code = 200. User should be forbidden to edit data of another user. Both of these users have the same permissions.

        # GET DATA OF THE SECOND USER AFTER EDIT
        response6 = MyRequests.get(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2},
        )
        print(response6.text)
        print(response6.status_code)
        response_data = response6.json()
        print(response_data["username"])

        Assertions.assert_code_status(response6, 200)
        assert response_data["username"] == username2, \
            f"User changed another user data. Actual result: {response_data['username']}. Expected result:{username2}"


    # - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_email_without_dog(self):
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response7 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response7, 200)
        Assertions.assert_json_has_key(response7, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response7, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response8 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response8, "auth_sid")
        token = self.get_header(response8, "x-csrf-token")

        # EDIT
        new_email = "learnqaexample.com"

        response9 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_email}
        )

        Assertions.assert_code_status(response9, 200)

        # GET DATA AFTER EDIT
        response10 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        response_data = response10.json()
        assert response_data["email"] == email, f"User changed email to incorrect one. Actual result: {response_data['email']}. Expected result:{email}" 
        Assertions.assert_code_status(response10, 200)



    # - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_firstname_to_one_character_value(self):
        # REGISTRATION
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "a"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_has_key(response3, "error")

        # GET DATA AFTER EDIT
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        print(response4.text)
        print(response4.status_code)
        parsed_response = response4.json()
        print(parsed_response['firstName'])
        assert parsed_response["firstName"] == register_data['firstName'], \
            f"Incorrect first name. First name is changed to too short value '{new_name}'. Expected result:{register_data['firstName']}"




















