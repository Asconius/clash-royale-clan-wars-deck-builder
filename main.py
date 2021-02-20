from datetime import datetime
from time import time

from clash_royale_api import clash_royale_api
from constants import CONFIG_INI, INITIAL_KEY, DEFAULT_SECTION, HASH_KEY, RATING_KEY, EXCLUDED_KEY, CARD_LIST_KEY, \
    DECKS_TXT, NEWLINE, INITIAL_SECTION, DECK_NUMBER, SOURCE_KEY
from royale_api import royale_api
from stats_royale import popular_decks, top_200_players
from utils import get_hash, config


def clash_royale_river_race_deck_builder():
    config.read(CONFIG_INI)
    initial = int(config[DEFAULT_SECTION][INITIAL_KEY])
    best_rating = float(config[DEFAULT_SECTION][RATING_KEY])
    best_hash = config[DEFAULT_SECTION][HASH_KEY]
    best_list = []
    deck_list = get_deck_list()
    initial_list = get_initial_list()

    for a in initial_list if initial else deck_list:
        for b in deck_list:
            for c in deck_list:
                for d in deck_list:
                    attempt_list = [a, b, c, d]
                    if compare_decks(attempt_list):
                        attempt_rating = sum(list(map(lambda i: i[RATING_KEY], attempt_list))) / DECK_NUMBER
                        attempt_hash = get_hash(list(map(lambda i: i[HASH_KEY], attempt_list)))

                        if attempt_hash == best_hash:
                            best_rating = attempt_rating
                            config[DEFAULT_SECTION][RATING_KEY] = str(best_rating)
                        elif attempt_rating > best_rating:
                            best_rating = attempt_rating
                            best_list = attempt_list
                            best_hash = attempt_hash
    if len(best_list) > 0:
        config[DEFAULT_SECTION][RATING_KEY] = str(best_rating)
        config[DEFAULT_SECTION][HASH_KEY] = best_hash
        write_config()
        best_list.sort(key=lambda i: i[RATING_KEY], reverse=True)
        write_file(best_rating, best_list)


def write_file(best_rating, attempt_list):
    with open(DECKS_TXT, 'a+') as file:
        file.write('{}{}'.format('#' * 80, NEWLINE))
        file.write('Time: {}{}'.format(timestamp(), NEWLINE))
        file.write('Overall Rating: {}%{}'.format(best_rating, NEWLINE))
        for attempt in attempt_list:
            file.write(NEWLINE)
            file.write('Rating: {}%{}'.format(attempt[RATING_KEY], NEWLINE))
            for card in attempt[CARD_LIST_KEY]:
                file.write(card + NEWLINE)
        file.close()


def write_config():
    with open(CONFIG_INI, 'w') as file:
        config.write(file)
        file.close()


def compare_decks(attempt_list):
    equal_number = 0
    for a in attempt_list:
        for b in attempt_list:
            if a[CARD_LIST_KEY] == b[CARD_LIST_KEY]:
                equal_number += 1
            else:
                for x in a[CARD_LIST_KEY]:
                    for y in b[CARD_LIST_KEY]:
                        if x == y:
                            return False
    return equal_number == len(attempt_list)


def timestamp():
    return datetime.fromtimestamp(time())


def get_initial_list():
    card_list = list(map(lambda i: i.strip(), config[INITIAL_SECTION][CARD_LIST_KEY].split(',')))
    initial_dict = {
        RATING_KEY: float(config[INITIAL_SECTION][RATING_KEY]),
        HASH_KEY: get_hash(card_list),
        CARD_LIST_KEY: card_list
    }
    return [initial_dict]


def get_deck_list():
    source = config[DEFAULT_SECTION][SOURCE_KEY]
    if source == 'popular decks':
        return filter_excluded(popular_decks())
    elif source == 'top 200 players':
        return filter_excluded(top_200_players())
    elif source == 'royale api':
        return filter_excluded(royale_api())
    elif source == 'clash royale api':
        return filter_excluded(clash_royale_api())


def filter_excluded(deck_list):
    excluded_list = list(map(lambda i: i.strip(), config[DEFAULT_SECTION][EXCLUDED_KEY].split(',')))
    return list(filter(lambda i: all(list(map(lambda j: j not in i[CARD_LIST_KEY], excluded_list))), deck_list))


if __name__ == '__main__':
    clash_royale_river_race_deck_builder()
