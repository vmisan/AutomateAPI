from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import json
import time

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        user = self.register()

        auth_sid, token = self.login(user.email, user.password)

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            f"Wrong name of the user after edit. Actual value: {user.first_name}. Expected value: {new_name}"
        )

    # Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_edit_by_unauthorized_user(self):
        user = self.register()

        # EDIT
        new_lastname = "Changed Last Name"

        response = MyRequests.put(
            f"/user/{user.user_id}",
            data={"lastName": new_lastname}
        )

        Assertions.assert_code_status(response, 400)
        assert response.text == "Auth token not supplied", "Response is changed when unauthorized user tries to edit"

    #     - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_user_cannot_edit_another_user_data(self):
        # REGISTRATION of the FIRST USER
        user1 = self.register()


        time.sleep(2) # Wait 2 seconds in order to get different email

        # REGISTRATION of the SECOND USER
        user2 = self.register()

        # LOGIN as the FIRST USER
        auth_sid, token = self.login(user1.email, user1.password)


        # LOGIN as the SECOND USER
        auth_sid2, token2 = self.login(user2.email, user2.password)


        # THE FIRST USER TRIES TO EDIT THE SECOND USER' DATA
        new_username = "Changed Username"

        response5 = MyRequests.put(
            f"/user/{user2.user_id}",
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
            f"/user/{user2.user_id}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2},
        )
        print(response6.text)
        print(response6.status_code)
        response_data = response6.json()
        print(response_data["username"])

        Assertions.assert_code_status(response6, 200)
        assert response_data["username"] == user2.username, \
            f"User changed another user data. Actual result: {response_data['username']}. Expected result:{user2.username}"


    # - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_edit_email_without_dog(self):
        user = self.register()
        auth_sid, token = self.login(user.email, user.password)

        # EDIT
        new_email = "learnqaexample.com"

        response9 = MyRequests.put(
            f"/user/{user.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_email}
        )

        Assertions.assert_code_status(response9, 200)

        # GET DATA AFTER EDIT
        response10 = MyRequests.get(
            f"/user/{user.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        response_data = response10.json()
        assert response_data["email"] == user.email, f"User changed email to incorrect one. Actual result: {response_data['email']}. Expected result:{user.email}"
        Assertions.assert_code_status(response10, 200)



    # - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_firstname_to_one_character_value(self):
        user = self.register()

        auth_sid, token = self.login(user.email, user.password)

        # EDIT
        new_name = "a"

        response3 = MyRequests.put(
            f"/user/{user.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_has_key(response3, "error")

        # GET DATA AFTER EDIT
        response4 = MyRequests.get(
            f"/user/{user.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        print(response4.text)
        print(response4.status_code)
        parsed_response = response4.json()
        print(parsed_response['firstName'])
        assert parsed_response["firstName"] == user.first_name, \
            f"Incorrect first name. First name is changed to too short value '{new_name}'. Expected result:{user.first_name}"




















