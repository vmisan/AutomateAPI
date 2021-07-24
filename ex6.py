import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect", allow_redirects = True)
all_redirects = response.history
print(f"All redirects {all_redirects}")
end_url = response.history[2]
print(f"{end_url.url} is the destination point of all these redirects")