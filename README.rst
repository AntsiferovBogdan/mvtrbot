Мувитрина
=====
Мувитрина - это бот, который выручит вас томным вечером, когда вам захочется посмотреть фильм в онлайн-кинотеатре, но не переплатить за это.
Бот анализирует цены на конкретный фильм на всех площадках и выдает лучший вариант. Также Мувитрина подскажет, если интересующий фильм будут транслировать по ТВ в ближайшее время :)

Установка
---------
Создайте и активируйте виртуальное окружение:

.. code-block:: text

    pip install -r requirements.txt

Настройка
---------
Создайте файл settings.py, добавьте следующие настройки:

.. code-block:: python

    PROXY = {'proxy_url': 'socks5://YOUR_SOCKS5_PROXY:1080',
        'urllib3_proxy_kwargs': {'username': 'LOGIN', 'password': 'PASSWORD'}}

    API_KEY = ('API_KEY FROM BOTFATHER')

    USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:', ':boy:', ':girl:',
                ':mouse:',':frog:',':tiger:',':new_moon_with_face:',':crown:',':alien:']

Запуск
-------

В активированном виртуальном окружении введите:

.. code-block:: text

    python bot.py