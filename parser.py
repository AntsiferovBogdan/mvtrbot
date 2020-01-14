import re
import requests

from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_price(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        movie_name = re.findall(r'\w*', soup.h1.string)
        print(movie_name[1])
    return False


html = get_html('https://okko.tv/movie/joker')
get_price(html)
