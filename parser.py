import logging
import re
import requests
import settings
import time

from telegram.ext import ConversationHandler
from utils import get_confirm_keyboard, get_keyboard

from bs4 import BeautifulSoup
from selenium import webdriver
from telegram import ReplyKeyboardRemove

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_PATH


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
    url = 'https://www.ivi.ru/search/?q=' + user_input_fix
    html_ivi = get_html(url)
    global i
    if html_ivi:
        global soup
        soup = BeautifulSoup(html_ivi, 'html.parser')
        global search_info_all
        search_info_all = soup.find_all(class_='nbl-slimPosterBlock__title')
        search_info = search_info_all[i]
        global info
        info = ''.join(re.findall(r'[а-я А-Я 0-9]', search_info.text))
        global search_poster
        search_poster = soup.find_all('li', class_='gallery__item')
        search_url = search_poster[i].find('a')
        global url_ivi
        url_ivi = 'ivi.ru' + search_url['href']
        search_poster = search_poster[i].find(class_='nbl-poster__image')
        global poster
        poster = search_poster['src'].split('.jpg')
        update.message.reply_text(
            f"Вас интересует данный фильм? '{info}' {poster[0]}.jpg",
            reply_markup=get_confirm_keyboard()
            )
        return 'confirm'


def get_url_ivi(bot, update):
    update.message.reply_text(
        'Ищу цены, подождите, пожалуйста...',
        reply_markup=ReplyKeyboardRemove()
        )
    driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH,
                              chrome_options=chrome_options
                              )
    driver.get('http://' + url_ivi)
    #try:
        #element_0 = driver.find_element_by_class_name(
                #'fullscreen-popup__close-view-button'
                #)
        #element_0.click()
    #finally:
    try:
        element_1 = driver.find_element_by_id('js-erotic-confirm')
        element_1.click()
    finally:
        element_2 = driver.find_element_by_class_name(
            'playerBlock__nbl-button_playerMainAction'
            )
        element_2.click()
    time.sleep(7)
    price_page = driver.page_source
    soup = BeautifulSoup(price_page, 'html.parser')
    subscribe = soup.find('h1')
    subscribe_in = ''.join((re.findall(r'[а-яА-Я]', subscribe.text)))
    if 'Подписка' in subscribe_in:
        update.message.reply_text(
            'Данный фильм доступен по подписке ivi. Также Вы можете приобрести его в HD/SD качестве за 399/299₽.',
            reply_markup=get_keyboard()
            )
    else:
        price_page = driver.page_source
        soup = BeautifulSoup(price_page, 'html.parser')
        search_prices = soup.find_all(class_='plateTile__caption')

        price_buy_hd = re.findall(r'\d', search_prices[0].text)
        price_buy_sd = re.findall(r'\d', search_prices[1].text)
        price_rent_hd = re.findall(r'\d', search_prices[2].text)
        price_rent_sd = re.findall(r'\d', search_prices[3].text)

        update.message.reply_text(
            f"Смотрите фильм '{info}' в онлайн-кинотеатре ivi: {url_ivi}"
            )
        update.message.reply_text(
            f"Купить фильм в HD/SD качестве - {(''.join(price_buy_hd))}₽/{(''.join(price_buy_sd))}₽, арендовать - {(''.join(price_rent_hd))}₽/{(''.join(price_rent_sd))}₽. При аренде фильма у Вас будет 30 дней, чтобы начать просмотр фильма, и 48 часов, чтобы закончить его.",
            reply_markup=get_keyboard()
            )
    return ConversationHandler.END


def incorrect_movie(bot, update):
    global i
    i += 1
    search_info_all = soup.find_all(class_='nbl-slimPosterBlock__title')
    search_info = search_info_all[i]
    info = ''.join(re.findall(r'[а-я А-Я0-9]', search_info.text))
    search_poster = soup.find_all('li', class_='gallery__item')
    search_url = search_poster[i].find('a')
    global url_ivi
    url_ivi = 'ivi.ru' + search_url['href']
    search_poster = search_poster[i].find(class_='nbl-poster__image')
    poster = search_poster['src'].split('.jpg')
    update.message.reply_text(
        f"Вас интересует данный фильм? '{info}' {poster[0]}.jpg",
        reply_markup=get_confirm_keyboard()
        )
    return 'confirm'


i = 0
url_ivi = None
