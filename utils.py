from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup

import settings


def get_user_emoji(user_data):
    if 'emoji' in user_data:
        return user_data['emoji']
    else:
        user_data['emoji'] = emojize(
            choice(settings.USER_EMOJI), use_aliases=True
            )
        return user_data['emoji']


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup(
        [['Зарегистрироваться'], ['Найти фильм']], resize_keyboard=True
        )
    return my_keyboard


def get_confirm_keyboard():
    my_keyboard_2 = ReplyKeyboardMarkup(
        [['Да'], ['Нет']], resize_keyboard=True
        )
    return my_keyboard_2
