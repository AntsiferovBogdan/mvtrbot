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


def get_movie_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    new_list = soup.find('', class_='')
    print(new_list)


if __name__ == '__main__':
    html = get_html('online_cinema_url')
    if html:
        with open('movies_price_list.html', 'w', encoding='utf8') as f:
            f.write(html)
