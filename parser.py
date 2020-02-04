import logging
import os
import re
import requests
import settings
import time

from utils import get_confirm_keyboard, get_keyboard

from telegram.ext import ConversationHandler

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from telegram import ReplyKeyboardRemove


def searching_start(bot, update):
    update.message.reply_text(
                              'Введите название фильма',
                              reply_markup=ReplyKeyboardRemove()
                              )
    return 'search_movie'


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def search_movie(bot, update):
    logging.info('user: %s, chat_id: %s, movie: %s',
                 update.message.chat.username,
                 update.message.chat.id,
                 update.message.text
                 )

    user_input_fix = '+'.join(update.message.text.split())
    url = 'https://www.kinopoisk.ru/index.php?kp_query=' + user_input_fix
    html_kp = get_html(url)
    global i
    i = 0
    if html_kp:
        global soup
        soup = BeautifulSoup(html_kp, 'html.parser')
        global search_info_kp
        search_info_kp = soup.find_all('p', class_='name')
        search_title_kp = search_info_kp[i].find('a')
        global title_kp
        title_kp = ''.join(re.findall(r'[а-я А-Я0-9I]', search_title_kp.text))
        search_year_kp = search_info_kp[i].find('span')
        year_kp = ''.join(re.findall(r'[0-9]', search_year_kp.text))
        search_poster_kp = soup.find_all(class_='pic')
        search_poster_kp = search_poster_kp[i].find(
            class_="js-serp-metrika").get('data-id')
        poster_kp = 'https://st.kp.yandex.net/images/film_iphone/iphone360_' + search_poster_kp + '.jpg'
        global search_director_kp
        search_director_kp = soup.find_all('i', class_='director')
        global director_kp
        director_kp = (''.join(re.findall(
            r'[а-я А-Я]', search_director_kp[i].text))
            ).split('реж ')
        update.message.reply_text(
            f'Вас интересует данный фильм? {title_kp}, {year_kp} {poster_kp}',
            reply_markup=get_confirm_keyboard()
            )
        return 'confirm'


def incorrect_movie(bot, update):
    global i
    i += 1
    search_title_kp = search_info_kp[i].find('a')
    global title_kp
    title_kp = ''.join(re.findall(r'[а-я А-Я0-9I]', search_title_kp.text))
    search_year_kp = search_info_kp[i].find('span')
    global year_kp
    year_kp = ''.join(re.findall(r'[0-9]', search_year_kp.text))
    search_poster_kp = soup.find_all(class_='pic')
    search_poster_kp = search_poster_kp[i].find(class_="js-serp-metrika").get(
        'data-id'
        )
    global poster_kp
    poster_kp = 'https://st.kp.yandex.net/images/film_iphone/iphone360_' + search_poster_kp + '.jpg'
    global director_kp
    director_kp = (''.join(re.findall(
        r'[а-я А-Я]', search_director_kp[i].text))
        ).split('реж ')
    update.message.reply_text(
        f'Вас интересует данный фильм? {title_kp}, {year_kp} {poster_kp}',
        reply_markup=get_confirm_keyboard()
        )
    return 'confirm'


def get_url_megogo(bot, update):
    title_fix = '+'.join(title_kp.split())
    url = 'https://megogo.ru/ru/search-extended?q=' + title_fix
    html_megogo = get_html(url)
    soup_megogo = BeautifulSoup(html_megogo, 'html.parser')

    search_info_megogo = soup_megogo.find_all('div', {'class': 'thumb'})
    global m
    title_megogo = search_info_megogo[m].find('a').find('img').get('alt')
    global url_megogo
    url_megogo = 'https://megogo.ru' + search_info_megogo[m].find('a').get('href')

    director_url_megogo = url_megogo + '?video_view_tab=cast'
    director_html_megogo = get_html(director_url_megogo)
    director_parsing_megogo = BeautifulSoup(
        director_html_megogo, 'html.parser'
        )
    director_search_megogo = director_parsing_megogo.find(
        class_='video-persons type-other').find(class_='video-person-name')
    director_megogo = ''.join(re.findall(
        r'[а-я А-Я]', director_search_megogo.text)
        )

    if title_kp == title_megogo and director_kp[1] == director_megogo:
        get_price_megogo(bot, update)
    else:
        m += 1
        get_url_megogo(bot, update)


def get_url_ivi(bot, update):
    title_fix = '+'.join(title_kp.split())
    url = 'https://www.ivi.ru/search/?q=' + title_fix
    print(url)
    html_ivi = get_html(url)
    soup_ivi = BeautifulSoup(html_ivi, 'html.parser')

    search_title_ivi = soup_ivi.find_all(class_='nbl-slimPosterBlock__title')
    global iv
    title_ivi = ''.join(re.findall(
        r'[а-я А-Я]', search_title_ivi[iv].text)
        )
    global url_ivi
    search_url_ivi = soup_ivi.find_all(class_='gallery__item')
    url_ivi = 'ivi.ru' + search_url_ivi[iv].find('a').get('href')
    director_url_ivi = url_ivi + '?video_view_tab=cast'
    director_html_ivi = get_html(director_url_ivi)
    director_parsing_ivi = BeautifulSoup(
        director_html_ivi, 'html.parser'
        )
    director_search_ivi = director_parsing_ivi.find(
        class_='personsLine__link')
    director_ivi = ''.join(re.findall(
        r'[а-я А-Я]', director_search_ivi.text)
        )
    print(director_ivi)
    #if title_kp == title_megogo and director_kp[1] == director_megogo:
        #get_price_megogo(bot, update)
    #else:
        #iv += 1
        #get_all_urls(bot, update)


def get_price_megogo(bot, update):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path=settings.CHROME_DRIVER_URL
        )
    driver.get(url_megogo)
    time.sleep(3)
    element_1 = driver.find_element_by_class_name('play-icon')
    element_1.click()
    time.sleep(2)
    price_page = driver.page_source
    soup_megogo_price = BeautifulSoup(price_page, 'html.parser')
    find_subscribe = soup_megogo_price.find('p', class_='stub-description')
    if 'доступен' in find_subscribe.text:
        update.message.reply_text(
            f'Фильм доступен по подписке'  # через re вытянуть полный текст с мегого
            )
    else:
        search_price = soup.find_all(class_='pQualityItemPrice__value')
        price_buy_hd = ''.join(re.findall(r'[0-9]', search_price[0].text))
        price_buy_sd = ''.join(re.findall(r'[0-9]', search_price[1].text))
        price_rent_hd = ''.join(re.findall(r'[0-9]', search_price[2].text))
        price_rent_sd = ''.join(re.findall(r'[0-9]', search_price[3].text))
        update.message.reply_text(
            f'Купить фильм в HD/SD-качестве - {price_buy_hd}/{price_buy_sd}₽, арендовать фильм в HD/SD-качестве - {price_rent_hd}/{price_rent_sd}₽'
            )


def get_url_ivi_2(bot, update):  # под удаление
    update.message.reply_text(
        'Ищу цены, подождите, пожалуйста...',
        reply_markup=ReplyKeyboardRemove()
        )
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path=settings.CHROME_DRIVER_URL, options=chrome_options
        )
    driver.get('http://' + url_ivi)
    time.sleep(5)
    logging.info

    try:
        element_1 = driver.find_element_by_id('js-erotic-confirm')
        element_1.click()
    except NoSuchElementException:
        element_0 = driver.find_element_by_class_name(
            'fullscreen-popup_has-close-view-button'
            )
        element_0.click()

    finally:
        time.sleep(3)
        price_page = driver.page_source
        soup = BeautifulSoup(price_page, 'html.parser')
        search_bell = soup.find_all(class_='nbl-button__primaryText')
        search_bell_in = ''.join((re.findall(r'[а-я А-Я]', search_bell[1].text)))
        if 'Сообщить о появлении' in search_bell_in:
            update.message.reply_text(
                'К сожалению, данный фильм отсутствует в онлайн-кинотеатре на текущий момент.',
                reply_markup=get_keyboard()
                )
            return ConversationHandler.END

        try:
            element_2 = driver.find_element_by_class_name(
                'playerBlock__nbl-button_playerMainAction'
                )
            element_2.click()
            time.sleep(5)

            price_page = driver.page_source
            soup = BeautifulSoup(price_page, 'html.parser')
            subscribe = soup.find('h1')
            subscribe_in = ''.join((re.findall(r'[а-яА-Я]', subscribe.text)))
            if 'Подписка' in subscribe_in:
                update.message.reply_text(
                    f"Смотрите фильм '{info}' в онлайн-кинотеатре ivi: {url_ivi}"
                    )
                update.message.reply_text(
                    'Данный фильм доступен по подписке ivi. Также Вы можете приобрести его в HD/SD качестве за 399/299₽.',
                    reply_markup=get_keyboard()
                    )
                return ConversationHandler.END

            else:
                price_page = driver.page_source
                soup = BeautifulSoup(price_page, 'html.parser')
                search_prices = soup.find_all(class_='plateTile__caption')
                update.message.reply_text(
                                f"Смотрите фильм '{info}' в онлайн-кинотеатре ivi: {url_ivi}"
                                )
                price_buy_hd = re.findall(r'\d', search_prices[0].text)
                update.message.reply_text(
                                f"Купить фильм в HD-качестве - {(''.join(price_buy_hd))}₽",
                                )
                price_buy_sd = re.findall(r'\d', search_prices[1].text)
                update.message.reply_text(
                                f"Купить фильм в SD-качестве - {(''.join(price_buy_sd))}₽",
                                )
                price_rent_hd = re.findall(r'\d', search_prices[2].text)
                update.message.reply_text(
                                f"Арендовать фильм в HD-качестве - {(''.join(price_rent_hd))}₽",
                                )
                price_rent_sd = re.findall(r'\d', search_prices[3].text)
                update.message.reply_text(
                                f"Арендовать фильм в SD-качестве - {(''.join(price_rent_sd))}₽",
                                )
                update.message.reply_text(
                    f"При аренде фильма у Вас будет 30 дней, чтобы начать просмотр фильма, и 48 часов, чтобы закончить его.",
                    reply_markup=get_keyboard()
                    )
                return ConversationHandler.END
        except NoSuchElementException:
            return 'greet_user'


i = 0
m = 0
iv = 0
title_kp = None
director_kp = None
