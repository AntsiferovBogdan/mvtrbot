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


def get_url_kp(url):
    html_kp = get_html(url)
    i = 2
    soup = BeautifulSoup(html_kp, 'html.parser')
    search_info = soup.find_all('p', class_='name')
    search_title = search_info[i].find('a')
    title = ''.join(re.findall(r'[а-я А-Я0-9I]', search_title.text))
    search_year = search_info[i].find('span')
    year = ''.join(re.findall(r'[0-9]', search_year.text))
    parsing_poster = soup.find_all(class_='pic')
    search_poster = parsing_poster[i].find(class_="js-serp-metrika").get(
        'data-id'
        )
    poster = 'https://st.kp.yandex.net/images/film_iphone/iphone360_' + search_poster + '.jpg'
    search_director = soup.find_all('i', class_='director')
    director = (''.join(re.findall(r'[а-я А-Я]', search_director[0].text))).split('реж ')
    print(
        f"Вас интересует данный фильм? {title}, {year} {poster}",
        'reply_markup=get_confirm_keyboard()'
        )
    return 'confirm'


user_input = input()
user_input_fix = '+'.join(user_input.split())
url = 'https://www.kinopoisk.ru/index.php?kp_query=' + user_input_fix
get_url_kp(url)
