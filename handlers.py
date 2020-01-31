import logging

# from model import Users, session
from utils import get_keyboard, get_user_emoji

# from sqlalchemy import create_engine
# from telegram import ReplyKeyboardRemove
# from telegram.ext import ConversationHandler

# import re
# import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    text = 'Привет, {} {}'.format(update.message.chat.first_name, emoji)
    update.message.reply_text(text, reply_markup=get_keyboard())


def dontknow(bot, update):
    update.message.reply_text('Проверьте корректность введенного e-mail')
    return 'email'
