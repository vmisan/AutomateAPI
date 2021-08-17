"""
В этой задаче нужно написать тест, который авторизовывается одним пользователем, но получает данные другого (т.е. с другим ID).
И убедиться, что в этом случае запрос также получает только username, так как мы не должны видеть остальные данные чужого пользователя.
"""

#My logic:
# Create 1 user
# Create 2 user > Get id of the second user
# Login as the first user > Verify presence "id" key only


import requests
import time
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

class TestAuthorizedUserDoesNotObserveAnotherUserDetailedInfo(BaseCase):
    def test_authorized_user_dont_observe_another_user_detailed_info(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"


        # 1. Sign up to the system as the first user
        sign_up_data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data= sign_up_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


        time.sleep(2) # Wait 2 seconds in order to get different email


        # 2. Sign up to the system as the second user
        random_part2 = datetime.now().strftime("%m%d%Y%H%M%S")
        email2 = f"{base_part}{random_part2}@{domain}"
        sign_up_data2 = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email2
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/", data=sign_up_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")


        # 3. Login to the system as the first registered user
        login_data = {
            'email': email,
            'password': '123'
        }

        response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # 4. Login to the system as the second registered user
        login_data2 = {
            'email': email2,
            'password': '123'
        }

        response4 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data2)

        user_id2_from_login_endpoint = self.get_json_value(response4, "user_id")

        # 5. Get another user data for logged in user
        response5 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id2_from_login_endpoint}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_json_has_key(response5, "username")
        Assertions.assert_json_has_not_key(response5, "email")
        Assertions.assert_json_has_not_key(response5, "firstName")
        Assertions.assert_json_has_not_key(response5, "lastName")