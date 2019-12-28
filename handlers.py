import logging

from utils import *

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def greet_user(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    text = 'Привет, {} {}'.format(update.message.chat.first_name, emoji)
    update.message.reply_text(text, reply_markup=get_keyboard())

def registration_start(bot, update, user_data):
	update.message.reply_text('Введите свой e-mail', reply_markup=ReplyKeyboardRemove())
	return 'email'

def registration_get_email(bot, update, user_data):
	user_email = update.message.text
	if '@' and '.' not in user_email:
		update.message.reply_text('Проверьте корректность введенного e-mail')
		return 'email'
	else:
		logging.info('User: %s, Chat ID: %s, E-Mail: %s', update.message.chat.username,
        update.message.chat.id, update.message.text)
		update.message.reply_text('Спасибо!')
	return ConversationHandler.END

def dontknow(bot, update, user_data):
    update.message.reply_text('Проверьте корректность введенного e-mail')
    return 'email'
