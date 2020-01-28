import logging
import re
import requests
import settings
import time

from telegram.ext import ConversationHandler
from utils import get_confirm_keyboard

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from telegram import ReplyKeyboardRemove


def searching_start(bot, update):
    update.message.reply_text(
                              'Введите название фильма',
                              reply_markup=ReplyKeyboardRemove()
                              )
    return 'ivi'


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_url_ivi(bot, update):
    logging.info('user: %s, chat_id: %s, movie: %s',
                 update.message.chat.username,
                 update.message.chat.id,
                 update.message.text
                 )
    user_input_fix = '+'.join(update.message.text.split())
    url = 'https://www.ivi.ru/search/?q=' + user_input_fix
    global html_ivi
    html_ivi = get_html(url)
    if html_ivi:
        soup = BeautifulSoup(html_ivi, 'html.parser')
        search_title = soup.find(class_='nbl-slimPosterBlock__title')
        global title
        title = ''.join(re.findall(r'[а-я А-Я0-9]', search_title.text))
        search_year = soup.find_all(class_='nbl-poster__propertiesRow')
        year = re.findall(r'\d{4}', search_year[1].text)
        search_poster = soup.find(class_='nbl-poster__image')
        poster = search_poster['src'].split('/172')
        if year:
            update.message.reply_text(
                f"Вас интересует данный фильм? {title}, {year[0]} {poster[0]}",
                reply_markup=get_confirm_keyboard()
                )
        else:
            year = re.findall(r'\d{4}', search_year[2].text)
            update.message.reply_text(
                f"Вас интересует данный фильм? {title}, {year[0]} {poster[0]}",
                reply_markup=get_confirm_keyboard()
                )
        return 'confirm'
    return False


def correct_movie(bot, update):
    update.message.reply_text(
        'Ищу цены, подождите, пожалуйста...',
        reply_markup=ReplyKeyboardRemove()
        )
    soup = BeautifulSoup(html_ivi, 'html.parser')
    search_url = soup.find('li', class_='gallery__item').find('a')
    list_ivi = []
    if search_url:
        list_ivi.append(search_url['href'])
    watch_ivi = 'ivi.ru' + list_ivi[0]
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
    #try:
        #element_3 = driver.find_element_by_class_name(class_="landing-table__button")
        #update.message.reply_text('Данный фильм Вы можете бесплатно посмотреть по подписке')
    except NoSuchElementException:
        print('упс')
    time.sleep(5)

    price_page = driver.page_source
    soup = BeautifulSoup(price_page, 'html.parser')
    search_prices = soup.find_all(class_='plateTile__caption')

    price_buy_hd = re.findall(r'\d', search_prices[0].text)
    price_buy_sd = re.findall(r'\d', search_prices[1].text)
    price_rent_hd = re.findall(r'\d', search_prices[2].text)
    price_rent_sd = re.findall(r'\d', search_prices[3].text)

    update.message.reply_text(
        f"Смотрите фильм '{title}' в онлайн-кинотеатре ivi: {watch_ivi}"
        )
    update.message.reply_text(f"Купить фильм в HD/SD качестве - {(''.join(price_buy_hd))}₽/{(''.join(price_buy_sd))}₽, арендовать - {(''.join(price_rent_hd))}₽/{(''.join(price_rent_sd))}₽. При аренде фильма у Вас будет 30 дней, чтобы начать просмотр фильма, и 48 часов, чтобы закончить его.")
    return ConversationHandler.END
