import logging

from utils import *

def greet_user(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    text = 'Привет {}'.format(emoji)
    update.message.reply_text(text)