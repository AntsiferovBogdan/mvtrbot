import logging

from model import Users, session
from utils import get_keyboard, get_user_emoji

from sqlalchemy import exists
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

import re

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    text = 'Привет, {} {}'.format(update.message.chat.first_name, emoji)
    update.message.reply_text(text, reply_markup=get_keyboard())


def registration_start(bot, update, user_data):
    update.message.reply_text(
                              'Введите свой e-mail',
                              reply_markup=ReplyKeyboardRemove()
                              )
    return 'email'


def registration_get_email(bot, update, user_data):
    user_email = update.message.text
    user_id = update.message.chat.id
    pattern = re.compile(
                         r'^[\w\.]+[-\w]+@+([\w]([-\w]{0,61}[\w])\.)+[a-zA-Z]{2,6}$'
                         )
    if re.match(pattern, user_email):
        logging.info('user: %s, chat_id: %s, email: %s',
                     update.message.chat.username,
                     update.message.chat.id,
                     update.message.text
                     )
        update.message.reply_text('Спасибо!')
        add_user(user_id, user_email)
    else:
        update.message.reply_text('Проверьте корректность введенного e-mail')
        return 'email'
    return ConversationHandler.END


def dontknow(bot, update, user_data):
    update.message.reply_text('Проверьте корректность введенного e-mail')
    return 'email'


def add_user(user_id, user_email):
    check_db = session.query(exists().where(Users.user_id == user_id)).scalar()
    if check_db is False:
        users = Users(user_id=user_id, user_email=user_email)
        session.add(users)
        session.commit()
    else:
        return ConversationHandler.END
