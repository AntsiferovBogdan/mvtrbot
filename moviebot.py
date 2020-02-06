import logging

from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters, ConversationHandler
                          )

from handlers import (check_email, greet_user,
                      registration_start, registration_get_email
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
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True,
                                  pass_chat_data=True)
                   )

    registration = ConversationHandler(
        entry_points=[(MessageHandler(Filters.regex('Зарегистрироваться'),
                      registration_start, pass_user_data=True,
                      pass_chat_data=True)
                       ),
                      (MessageHandler(Filters.regex('Найти фильм'),
                       searching_start, pass_user_data=True,
                       pass_chat_data=True)
                       )
                      ],
        states={
            'email': [MessageHandler(Filters.text, registration_get_email,
                                     pass_user_data=True, pass_chat_data=True)
                      ],
            'search_movie': [MessageHandler(Filters.text, search_movie,
                                            pass_user_data=True,
                                            pass_chat_data=True)
                             ],
            'confirm': [(MessageHandler(Filters.regex('Да'),
                        get_url_ivi, pass_user_data=True,
                        pass_chat_data=True)),
                        (MessageHandler(Filters.regex('Нет'),
                         incorrect_movie, pass_user_data=True,
                         pass_chat_data=True))
                        ]
        },
        fallbacks=[MessageHandler(
                                  Filters.photo | Filters.video |
                                  Filters.document, check_email
                                  )]
    )
    dp.add_handler(registration)

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
