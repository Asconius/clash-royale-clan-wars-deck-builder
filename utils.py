from configparser import ConfigParser
from hashlib import md5

from constants import EMPTY, DEFAULT_SECTION, LOG_KEY

config = ConfigParser()


def get_hash(card_list):
    return md5(EMPTY.join(sorted(card_list)).encode()).hexdigest()


def log(msg, *args, **kwargs):
    if int(config[DEFAULT_SECTION][LOG_KEY]):
        print(msg.format(*args, **kwargs))
