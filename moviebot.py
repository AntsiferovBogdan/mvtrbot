import logging

from telegram.ext import (Updater, CommandHandler, 
            MessageHandler, Filters, ConversationHandler)

from handlers import *
import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запускается')
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    
    registration = ConversationHandler(
        entry_points=[(MessageHandler(Filters.regex('Зарегистрироваться'), registration_start, pass_user_data=True))],
        states={
            'email': [MessageHandler(Filters.text, registration_get_email, pass_user_data=True)]
        },
        fallbacks=[MessageHandler(Filters.photo | Filters.video | Filters.document, dontknow, pass_user_data=True)]
    )
    dp.add_handler(registration)


    mybot.start_polling()
    mybot.idle()


if __name__=="__main__":
    main()
