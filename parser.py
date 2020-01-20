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


def get_url_ivi(html_ivi):
    if html_ivi:
        soup = BeautifulSoup(html_ivi, 'html.parser')
        search = soup.find('li', class_='gallery__item').find('a')
        list_ = []
        if search:
            list_.append(search['href'])
        print(f'Смотрите фильм {user_input.capitalize()} в онлайн-кинотеатре ivi: ivi.ru{list_[0]}')
    return False


def get_url_megogo(html_megogo):
    if html_megogo:
        soup = BeautifulSoup(html_megogo, 'html.parser')
        search = soup.find('div', class_='card-content video-content').find('a')
        list_ = []
        if search:
            list_.append(search['href'])
        print(f'Смотрите фильм {user_input.capitalize()} в онлайн-кинотеатре megogo: megogo.ru{list_[0]}')
    return False


user_input = input()
user_input_del_spaces = user_input.split()
user_input_no_spaces = '-'.join(user_input_del_spaces)

html_ivi = get_html('https://www.ivi.ru/search/?q=' + user_input_no_spaces)
html_megogo = get_html('https://megogo.ru/ru/search-extended?q=' + user_input_no_spaces)

get_url_ivi(html_ivi)
get_url_megogo(html_megogo)
