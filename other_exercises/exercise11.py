import requests

def test_homework_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print(dict(response.cookies))
    assert dict(response.cookies)["HomeWork"] == "hw_value", f"Cookie 'HomeWork' value is not {dict(response.cookies)['Homework']}"