import os

basedir = os.path.abspath(os.path.dirname(__file__))

PROXY = {'proxy_url': 'socks5://t2.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}
         }

API_KEY = ('907137899:AAE3njkeOX3agXvToU-G3vIXMGPFdTaZ4NY')

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:',
              ':dog:', ':boy:', ':girl:', ':mouse:', ':frog:', ':tiger:',
              ':new_moon_with_face:', ':crown:', ':alien:'
              ]

SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'users_db.db'

CHROME_DRIVER_URL = '/Users/dianaraddats/projects/MovieBot/chromedriver'

SAFARI_DRIVER_URL = '/usr/bin/safaridriver'

MONGO_LINK = 'mongodb+srv://mvtrbot:Rainn17.@cluster0-yanny.mongodb.net/mvtrbot?retryWrites=true&w=majority'

MONGO_DB = 'mvtrbot'
