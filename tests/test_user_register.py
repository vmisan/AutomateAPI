import pytest
import requests
import time


class TestUserRegister():
    parametrized_data = [
        (
            None,
            "learnqa",
            "learnqa",
            "learnqa",
            "vinkotov@example.com"
        ),
        (
            "123",
            None,
            "learnqa",
            "learnqa",
            "vinkotov@example.com"
        ),
        (
            "123",
            "learnqa",
            None,
            "learnqa",
            "vinkotov@example.com"
        ),
        (
            "123",
            "learnqa",
            "learnqa",
            None,
            "vinkotov@example.com"
        ),
        (
            "123",
            "learnqa",
            "learnqa",
            "learnqa",
            None
        )
    ]

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"


    def test_create_user_with_incorrect_email(self):
        # Email doesn't contain @
        incorrect_emaiL = email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': incorrect_emaiL
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response.text}"


    def test_create_user_with_short_username(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': '1',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('password, username, firstName, lastName, email', parametrized_data)
    def test_create_user_without_required_parameter(self, password, username, firstName, lastName, email):
        data = {
            'password': password,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        cut_response = response.text.startswith("The following required params are missed:")
        assert response.text.startswith("The following required params are missed:") == cut_response, f"Unexpected response content {response.text}"

    def test_create_user_with_long_username(self):
        user_name = "a"
        long_user_name = user_name * 250
        timestamp = time.time()  # timestamp stores the time in seconds
        # convert float to string type
        timestamp_string = str(timestamp)
        # print(type(timestamp_string))
        # create unique email
        email = 'vinkotov@example.com'
        unique_email = timestamp_string + email
        # print(unique_email)
        data = {
            'password': '123',
            'username': long_user_name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': unique_email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        assert "id" in response.json(), "There is no 'id' key in the response"

        # It's unclear how to clear data base after new user creation (how to remove just created user) after this home work



