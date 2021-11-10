import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

print(len(response.history))
print(response.url)
