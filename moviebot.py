import logging

from telegram.ext import (Updater, CommandHandler, 
            MessageHandler, Filters)

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
    
    
    mybot.start_polling()
    mybot.idle()


if __name__=="__main__":
    main()
