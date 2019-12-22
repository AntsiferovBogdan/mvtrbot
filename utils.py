from random import choice

from emoji import emojize

import settings

def get_user_emoji(user_data):
    if 'emoji' in user_data:
        return user_data['emoji']
    else:
        user_data['emoji'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emoji']