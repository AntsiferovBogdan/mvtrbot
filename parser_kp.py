import re
import requests
import settings
import time


from bs4 import BeautifulSoup
from selenium import webdriver


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_url_kp(html_kp):
    if html_kp:
        soup = BeautifulSoup(html_kp, 'html.parser')
        search_info = soup.find(class_='name')
        global info
        info = ''.join(re.findall(r'[а-я А-Я0-9]', search_info.text))
        search_poster = soup.find(class_='pic').find(class_="js-serp-metrika")
        global poster
        poster = search_poster['data-id']
        print(
            f"Вас интересует данный фильм? {info[:-5]}, {info[-4:]} https://st.kp.yandex.net/images/film_iphone/iphone360_{poster}.jpg",
            'reply_markup=get_confirm_keyboard()'
            )
        return 'confirm'
    return False


def correct_movie(html_kp_2):
    if html_kp_2:
        print(
            'Ищу цены, подождите, пожалуйста...',
            'reply_markup=ReplyKeyboardRemove()'
            )
        driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER_URL)
        driver.get('https://www.kinopoisk.ru/film/' + poster)
        element_1 = driver.find_element_by_class_name('kinopoisk-watch-online-button-partial-component kinopoisk-watch-online-button-partial-component_theme_desktop')
        element_1.click()
    time.sleep(5)

    price_page = driver.page_source
    soup = BeautifulSoup(price_page, 'html.parser')
    search_prices = soup.find_all(class_='PriceBlock__content--1RjcV')
    print(search_prices)
    price_buy_hd = re.findall(r'\d', search_prices[0].text)
    price_rent_hd = re.findall(r'\d', search_prices[2].text)

    print(
        f"Смотрите фильм '{info[:-5]}' в онлайн-кинотеатре КиноПоиск HD: {price_page}"
        )


user_input = input()
user_input_fix = '+'.join(user_input.split())
url = 'https://www.kinopoisk.ru/index.php?kp_query=' + user_input_fix
html_kp = get_html(url)
get_url_kp(html_kp)
html_kp_2 = get_html('https://www.kinopoisk.ru/film/' + poster)
correct_movie(html_kp_2)
