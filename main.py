import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


API_URL = "https://api.vk.com/method/"
API_VERSION = "5.199"


def shorten_link(access_token, url):
    response = requests.get(
        "{}utils.getShortLink".format(API_URL),
        params={
            "access_token": access_token,
            "v": API_VERSION,
            "url": url
        }
    )
    response.raise_for_status()

    vk_response = response.json()

    if "error" in vk_response:
        raise RuntimeError("Вы ввели неправильную ссылку")
    return vk_response["response"]["short_url"]


def count_clicks(access_token, short_url):
    parsed_url = urlparse(short_url)
    key = parsed_url.path.lstrip("/")

    response = requests.get(
        "{}utils.getLinkStats".format(API_URL),
        params={
            "access_token": access_token,
            "v": API_VERSION,
            "key": key,
            "extended": 1
        }
    )
    response.raise_for_status()
    stats_response = response.json()

    if "error" in stats_response:
        raise RuntimeError(stats_response["error"]["error_msg"])

    stats = stats_response["response"]["stats"]
    return sum(stat["views"] for stat in stats)


def is_shorten_link(access_token, url):
    parsed_url = urlparse(url)
    key = parsed_url.path.lstrip("/")

    response = requests.get(
        "{}utils.getLinkStats".format(API_URL),
        params={
            "access_token": access_token,
            "v": API_VERSION,
            "key": key,
            "extended": 1
        }
    )
    response.raise_for_status()
    vk_response = response.json()

    return "error" not in vk_response


def main():
    load_dotenv()
    access_token = os.environ["VK_ACCESS_TOKEN"]

    user_url = input("Введите ссылку для сокращения: ")

    try:
        if is_shorten_link(access_token, user_url):
            clicks = count_clicks(access_token, user_url)
            print("Всего переходов:", clicks)
        else:
            short_url = shorten_link(access_token, user_url)
            print("Сокращённая ссылка:", short_url)

    except (requests.exceptions.HTTPError, RuntimeError) as error:
        print("Ошибка:", error)


if __name__ == "__main__":
    main()
