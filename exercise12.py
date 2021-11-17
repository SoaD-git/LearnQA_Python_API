import requests


def test_homework_headers():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print(response.headers)
    print(response.headers["Set-Cookie"])
    assert "HomeWork=hw_value" in response.headers["Set-Cookie"],\
           "Set-Cookie header 'HomeWork=hw_value' not in response headers"
