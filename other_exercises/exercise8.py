import requests
import time

# 1. Создаем задачу
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

# Получаем токен и время выполнения задачи
token = response.json()["token"]
waiting_time = response.json()["seconds"]

# 2. Отправляем повторный запрос с токеном до того как задача готова, проверяем статус
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": f"{token}"})
status = "Job is ready"
if response.json()["status"] == "Job is NOT ready":
    status = "Job is NOT ready"
print(f"Статус выполнения: {status}")

# 3. Ставим на ожидание
time.sleep(waiting_time)

# 4. Отправляем запрос после ожидания исполнения задачи
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": f"{token}"})
status = "Job is ready"
if response.json()["status"] == "Job is NOT ready":
    status = "Job is NOT ready"
print(f"Статус выполнения: {status}, результат: {response.json()['result']}")

