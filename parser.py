import re
import requests
import time
import settings

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


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
        search_title = soup.find(class_='nbl-slimPosterBlock__title')
        title = ''.join(re.findall(r'[а-я А-Я0-9]', search_title.text))
        search_year = soup.find_all(class_='nbl-poster__propertiesRow')
        year = re.findall(r'\d{4}', search_year[1].text)
        search_poster = soup.find(class_='nbl-poster__image')
        poster = search_poster['src'].split('/172')
        if year:
            print(
                f"Вас интересует данный фильм? {title}, {year[0]} {poster[0]}"
                )
        else:
            year = re.findall(r'\d{4}', search_year[2].text)
            print(
                f"Вас интересует данный фильм? {title}, {year[0]} {poster[0]}"
                )

        search_url = soup.find('li', class_='gallery__item').find('a')
        list_ivi = []

        if search_url:
            list_ivi.append(search_url['href'])
        watch_ivi = 'ivi.ru' + list_ivi[0]
        print(f"Смотрите фильм '{title}' в онлайн-кинотеатре ivi: {watch_ivi}")

        driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER_URL)
        driver.get('http://' + watch_ivi)
        try:
            element_1 = driver.find_element_by_id('js-erotic-confirm')
            element_1.click()
        except NoSuchElementException:
            element_2 = driver.find_element_by_class_name(
                'playerBlock__nbl-button_playerMainAction'
                )
            element_2.click()
        time.sleep(10)

        price_page = driver.page_source
        soup = BeautifulSoup(price_page, 'html.parser')
        search_prices = soup.find_all(class_='plateTile__caption')

        price_buy_hd = re.findall(r'\d', search_prices[0].text)
        price_buy_sd = re.findall(r'\d', search_prices[1].text)
        price_rent_hd = re.findall(r'\d', search_prices[2].text)
        price_rent_sd = re.findall(r'\d', search_prices[3].text)

        print(f"Купить фильм в HD/SD качестве - {(''.join(price_buy_hd))}₽/{(''.join(price_buy_sd))}₽, арендовать - {(''.join(price_rent_hd))}₽/{(''.join(price_rent_sd))}₽. При аренде фильма у Вас будет 30 дней, чтобы начать просмотр фильма, и 48 часов, чтобы закончить его.")

    return False


def get_url_megogo(html_megogo):
    if html_megogo:
        soup = BeautifulSoup(html_megogo, 'html.parser')
        search = soup.find('div',
                           class_='card-content video-content').find('a')
        list_megogo = []
        if search:
            list_megogo.append(search['href'])
        watch_megogo = 'megogo.ru' + list_megogo[0]
        print(f'Смотрите {user_input.capitalize()} в онлайн-кинотеатре megogo: {watch_megogo}')

        driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER_URL)
        driver.get('http://' + watch_megogo)
        element = driver.find_element_by_xpath(
            "//button[@class='btn type-fill watch']"
            )
        time.sleep(5)
        print(element)

        # price_page = driver.page_source
        # soup = BeautifulSoup(price_page, 'html.parser')
        # search = soup.find(class_='plateTile__caption')
        # print(search)
    return False


user_input = input()
user_input_fix = '+'.join(user_input.split())

html_ivi = get_html(
    'https://www.ivi.ru/search/?q=' + user_input_fix
    )
# html_megogo = get_html(
    # 'https://megogo.ru/ru/search-extended?q=' + user_input_fix
    # )

get_url_ivi(html_ivi)
# get_url_megogo(html_megogo)
