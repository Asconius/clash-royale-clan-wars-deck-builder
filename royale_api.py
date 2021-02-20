from bs4 import BeautifulSoup
from requests import get

from constants import CARD_LIST_KEY, RATING_KEY, HASH_KEY, EMPTY
from utils import log, get_hash


def royale_api():
    deck_list = []
    response = get('https://royaleapi.com/decks/popular?time=1d&players=PvP&type=All&size=50&sort=win'
                   '&max_trophies=10000&min_elixir=1&max_elixir=9&mode=digest')
    soup = BeautifulSoup(response.text, features='lxml')
    elements = soup.find_all('div', {'class': 'ui attached segment deck_segment'})
    for element in elements:
        soup = BeautifulSoup(str(element), features='lxml')
        rating_element = soup.find('td', {'class': 'strong'})
        log(rating_element.text.strip())
        soup = BeautifulSoup(str(element), features='lxml')
        card_elements = soup.find_all('img')
        card_list = []
        for card_element in card_elements:
            card = card_element['alt']
            log(card)
            card_list.append(card)

        deck_dict = {
            RATING_KEY: float(rating_element.text.strip().replace('%', EMPTY)),
            HASH_KEY: get_hash(card_list),
            CARD_LIST_KEY: card_list,
        }
        deck_list.append(deck_dict)
    return deck_list
