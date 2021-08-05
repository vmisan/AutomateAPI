import requests

class TestGetCookie:
    def test_get_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        cookie = response.cookies
        print(dict(cookie))
        actual_cookie_value = cookie["HomeWork"]
        print(actual_cookie_value)
        expected_value = "hw_value"

        assert actual_cookie_value == expected_value, "Incorrect actual cookie value"
        assert response.status_code == 200, "Status code is incorrect"