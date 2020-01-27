import requests
import time
import settings

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


def get_url_ivi(html_ivi):
    if html_ivi:
        soup = BeautifulSoup(html_ivi, 'html.parser')
        search = soup.find('li', class_='gallery__item').find('a')
        list_ivi = []

        if search:
            list_ivi.append(search['href'])
        watch_ivi = 'ivi.ru' + list_ivi[0]
        print(f'Смотрите {user_input.capitalize()} в онлайн-кинотеатре ivi: {watch_ivi}')

        driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER_URL)
        driver.get('http://' + watch_ivi)
        element = driver.find_element_by_id('js-erotic-confirm')
        element.click()
        element = driver.find_element_by_class_name(
            'playerBlock__nbl-button_playerMainAction'
            )
        time.sleep(3)
        print(element)

        # price_page = driver.page_source
        # soup = BeautifulSoup(price_page, 'html.parser')
        # search = soup.find(class_='plateTile__caption')
        # print(search)
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
