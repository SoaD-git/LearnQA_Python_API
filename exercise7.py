import requests

# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "POST"})
print(response.text)

# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": "GET"})
print(response.text)

# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method. Например с
# GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. И так для
# всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.

method = ["GET", "POST", "PUT", "DELETE"]

for i in method:
    for j in method:
        if i == "GET":
            response = requests.request(method=i, url="https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method": f"{j}"}, headers=headers)
            print(i, j, response.text)
        else:
            response = requests.request(method=i, url="https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": f"{j}"}, headers=headers)
            print(i, j, response.text)

