import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


load_dotenv()


API_URL = "https://api.vk.com/method/"
API_VERSION = "5.199"


def get_service_time(access_token):
    response = requests.get(
        API_URL + "utils.getServerTime",
        params={
            "access_token": access_token,
            "v": API_VERSION
        }
    )
    response.raise_for_status()
    return response.json()


def shorten_link(access_token, url):
    response = requests.get(
        API_URL + "utils.getShortLink",
        params={
            "access_token": access_token,
            "v": API_VERSION,
            "url": url
        }
    )
    response.raise_for_status()

    response_data = response.json()

    if "error" in response_data:
        raise RuntimeError("Вы ввели неправильную ссылку")
    return response.json()["response"]["short_url"]


def count_clicks(access_token, short_url):
    parsed_url = urlparse(short_url)
    key = parsed_url.path.lstrip("/")

    response = requests.get(
        API_URL + "utils.getLinkStats",
        params={
            "access_token": access_token,
            "v": API_VERSION,
            "key": key,
            "extended": 1
        }
    )
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"]["error_msg"])

    stats = data["response"]["stats"]
    return sum(stat["views"] for stat in stats)


def is_shorten_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "vk.cc" and parsed_url.path != ""


def main():
    access_token = os.getenv("VK_ACCESS_TOKEN")

    print(get_service_time(access_token))

    user_url = input("Введите ссылку для сокращения: ")

    try:
        if is_shorten_link(user_url):
            clicks = count_clicks(access_token, user_url)
            print("Всего переходов:", clicks)
        else:
            short_url = shorten_link(access_token, user_url)
            print("Сокращённая ссылка:", short_url)

    except (requests.exceptions.HTTPError, RuntimeError) as error:
        print("Ошибка:", error)


if __name__ == "__main__":
    main()
