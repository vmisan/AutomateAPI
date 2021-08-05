import requests
class TestGetHeaders:
    def test_get_headers(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        print(response.headers["x-secret-homework-header"])
        actual_header_value = response.headers["x-secret-homework-header"]
        expected_header_value = "Some secret value"
        assert actual_header_value == expected_header_value, "Value in secret hieder is incorrect"
