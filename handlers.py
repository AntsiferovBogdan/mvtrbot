import logging

from model import Users, session
from parser import searching_start
from utils import get_keyboard, get_user_emoji

from sqlalchemy import create_engine
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

import re
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data, chat_data):
    emoji = get_user_emoji(user_data)
    text = f'Привет, {update.message.chat.first_name} {emoji}'
    update.message.reply_text(text, reply_markup=get_keyboard())


def registration_start(bot, update, user_data, chat_data):
    update.message.reply_text(
                              'Введите свой e-mail',
                              reply_markup=ReplyKeyboardRemove()
                              )
    return 'email'


def registration_get_email(bot, update, user_data, chat_data):
    user_email = update.message.text
    pattern = re.compile(
                         r'^[\w\.]+[-\w]+@+([\w]([-\w]{0,61}[\w])\.)+[a-zA-Z]{2,6}$'
                         )
    if re.match(pattern, user_email):
        logging.info('user: %s, chat_id: %s, email: %s',
                     update.message.chat.username,
                     update.message.chat.id,
                     update.message.text
                     )
        add_user(bot, update)
    elif user_email == 'Найти фильм':
        searching_start(bot, update, user_data)
    else:
        update.message.reply_text('Проверьте корректность введенного e-mail')
        return 'email'


def check_email(bot, update):
    update.message.reply_text('Введите, пожалуйста, текст.')
    return 'email'


def add_user(bot, update, user_data, chat_data):
    user_email = update.message.text
    user_id = update.message.chat.id

    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    connect = engine.connect()
    check_user = connect.execute('SELECT * FROM Users')

    for user in check_user:
        if user[1] == user_id:
            update.message.reply_text('Вы уже зарегистрированы.')
            return ConversationHandler.END
        elif user[2] == user_email:
            update.message.reply_text(
                'Данный e-mail уже используется, введите другой адрес.'
                )
            return 'email'

    users = Users(user_id=user_id, user_email=user_email)
    session.add(users)
    session.commit()
    update.message.reply_text('Спасибо!')
    return ConversationHandler.END
