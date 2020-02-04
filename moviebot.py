import logging

from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters, ConversationHandler
                          )

from handlers import (greet_user, registration_start,
                      registration_get_email, dontknow
                      )

from parser import (incorrect_movie, get_url_ivi, get_url_megogo,
                    search_movie, searching_start)

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
        entry_points=[(MessageHandler(Filters.regex('Зарегистрироваться'),
                      registration_start)),
                      (MessageHandler(Filters.regex('Найти фильм'),
                       searching_start))
                      ],
        states={
            'email': [MessageHandler(Filters.text, registration_get_email)
                      ],
            'search_movie': [MessageHandler(Filters.text, search_movie)
                             ],
            'confirm': [(MessageHandler(Filters.regex('Да'),
                        get_url_megogo)),
                        (MessageHandler(Filters.regex('Нет'),
                         incorrect_movie))
                        ]
        },
        fallbacks=[MessageHandler(
                                  Filters.photo | Filters.video |
                                  Filters.document, dontknow
                                  )]
    )
    dp.add_handler(registration)

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
