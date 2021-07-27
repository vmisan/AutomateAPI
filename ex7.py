import requests

# without "method" parameter
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

# request with nonexistent HEAD method
method_head= {"method":"HEAD"}
response_head = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method_head)
print(response_head.text)

# correct GET request
method_get = {"method":"GET"}
response2 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=method_get)
print(response2.text)

# correct POST request
method_post = {"method":"POST"}
response3 = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=method_post)
print(response3.text)

methods_list = ["GET", "POST", "PUT", "DELETE"]
parameters_methods_list = [{"method":"GET"}, {"method":"POST"}, {"method":"PUT"}, {"method":"DELETE"}]
for param in parameters_methods_list:

        result = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
        print(f"method GET with parameter params={param} has result with status code {result.status_code} and body {result.text}")
        result = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
        print(f"method POST with parameter data={param} has result with status code {result.status_code} and body {result.text}")
        result = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
        print(f"method PUT with parameter data={param} has result with status code {result.status_code} and body {result.text}")
        result = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
        print(f"method DELETE with parameter data={param} has result with status code {result.status_code} and body {result.text}")

#Answer: method DELETE with parameter data={'method': 'GET'} has result with status code 200 and body {"success":"!"}
