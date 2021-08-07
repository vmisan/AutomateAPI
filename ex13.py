import pytest
import requests

class TestGetUserAgent:
    data = [
        (
            "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mobile",
            "No",
            "Android"
        ),
        (
            "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
            "Mobile",
            "Chrome",
            "iOS"
        ),
        (
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Googlebot",
            "Unknown",
            "Unknown"
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            "Googlebot",
            "Chrome",
            "No"
        ),
        (
            "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "Mobile",
            "No",
            "iPhone"
        )
    ]
    @pytest.mark.parametrize('agent, platform, browser, device', data)
    def test_get_user_agent(self, agent, platform, browser, device):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        data = {"user-agent": agent}

        response = requests.get(url, headers=data)
        parsed_response = response.json()
        print(parsed_response)
        assert agent == parsed_response["user_agent"], f"Incorrect {agent} in response"
        assert platform == parsed_response["platform"], f"Response contains incorrect {platform} platform for typed {agent} user_agent"
        assert browser == parsed_response["browser"], f"Response contains incorrect {browser} browser for typed {agent} user_agent"
        assert device == parsed_response["device"], f"Response contains incorrect {device} device for typed {agent} user_agent"


