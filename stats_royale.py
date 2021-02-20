from bs4 import BeautifulSoup
from requests import get

from constants import RATING_KEY, CARD_LIST_KEY, EMPTY, SPACE, HASH_KEY
from utils import get_hash, log


def popular_decks():
    deck_list = []
    response = get('https://statsroyale.com/decks/popular')
    soup = BeautifulSoup(response.text, features='lxml')
    elements = soup.find_all('div', {'class': 'popularDecks_deckWrapper'})
    for element in elements:
        soup = BeautifulSoup(str(element), features='lxml')
        rating_element = soup.find('div', {'class': 'ui__headerBig'})
        log(rating_element.text.strip())
        soup = BeautifulSoup(str(element), features='lxml')
        deck_elements = soup.find_all('div', {'class': 'popularDecks__decklist'})
        soup = BeautifulSoup(str(deck_elements), features='lxml')
        card_elements = soup.find_all('a', href=True)
        card_list = []
        for card_element in card_elements:
            card = card_element['href'].replace('https://statsroyale.com/card/', EMPTY).replace('+', SPACE)
            log(card)
            card_list.append(card)

        deck_dict = {
            RATING_KEY: float(rating_element.text.strip().replace('%', EMPTY)),
            HASH_KEY: get_hash(card_list),
            CARD_LIST_KEY: card_list,
        }
        deck_list.append(deck_dict)
    return deck_list


def top_200_players():
    urls = ['https://statsroyale.com/decks/challenge-winners?type=top200&page={}'.format(i) for i in range(1, 7)]
    deck_list = []
    for i, url in enumerate(urls):
        response = get(url)
        soup = BeautifulSoup(response.text, features='lxml')
        elements = soup.find_all('div', {'class': 'recentWinners__decklist'})
        for j, element in enumerate(elements):
            soup = BeautifulSoup(str(element), features='lxml')
            card_elements = soup.find_all('a', href=True)
            card_list = []
            for card_element in card_elements:
                card = card_element['href'].replace('https://statsroyale.com/card/', EMPTY).replace('+', SPACE)
                log(card)
                card_list.append(card)

            deck_dict = {
                RATING_KEY: float(100 - i * 9 - j),
                HASH_KEY: get_hash(card_list),
                CARD_LIST_KEY: card_list,
            }
            deck_list.append(deck_dict)
    return deck_list
