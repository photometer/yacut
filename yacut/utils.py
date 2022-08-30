from random import choice
from string import ascii_letters, digits

from .models import URL_map


def get_unique_short_id():
    letters_digits = ascii_letters + digits
    random_string = ''.join(
        choice(letters_digits) for _ in range(6)
    )
    if URL_map.query.filter_by(short=random_string).first():
        # Это ведь рекурсивный вызов. Пока значение неуникально, глубина
        # рекурсии увеличивается.
        random_string = get_unique_short_id()
    return random_string
