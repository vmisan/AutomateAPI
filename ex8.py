import requests
import json
import time


response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
# Parse response body
parsed_response = response.json()
print(parsed_response)
token = parsed_response["token"]
print(token)
print(type(token))
responseUntilFinishedJob = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":{token}})

# Verify whether we have correct response when job is not finished
if responseUntilFinishedJob.json()["status"] == "Job is NOT ready":
        print("Correct status when job is not finished")
else:
        print("Incorrect response when job is not finished")

# Wait 10 seconds
time.sleep(10)

# Verify whether we have correct response when job is finished
responseForFinishedJob = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":{token}})
if responseForFinishedJob.json()["status"] == "Job is ready":
        print("Correct status when job is finished")
else:
        print("Incorrect response when job is  finished")
print(responseForFinishedJob.text)

#Verify "result" key presence in response when job is finished
obj = responseForFinishedJob.json()
key = "result"
if key in obj:
        print(f"Response when job is finished contains {key} key")
else:
        print(f"Response when job is finished doesn't contain {key} key")

