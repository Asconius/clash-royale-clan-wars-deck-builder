import os

from pyroyale import Configuration, LocationsApi, ClansApi, ApiClient, PlayersApi
from pyroyale.rest import ApiException

from constants import CARD_NUMBER, RATING_KEY, CARD_LIST_KEY, HASH_KEY, SUFFICIENT_DATA
from utils import log, get_hash


def clash_royale_api():
    ratio_dict = {}
    deck_dict, win_dict, loose_dict = fetch_battle_data()

    for key in deck_dict.keys():
        if has_sufficient_data(win_dict, key) and has_sufficient_data(loose_dict, key):
            ratio_dict[key] = win_dict[key] / loose_dict[key]

    sorted_ratio_dict = {k: v for k, v in sorted(ratio_dict.items(), key=lambda item: item[1])}
    log(len(sorted_ratio_dict))
    deck_list = []
    for key, value in sorted_ratio_dict.items():
        card_list = deck_dict[key]
        log(card_list, value)
        deck_list.append({RATING_KEY: value, HASH_KEY: key, CARD_LIST_KEY: card_list})
    return deck_list[-50:]


def fetch_battle_data():
    deck_dict = {}
    win_dict = {}
    loose_dict = {}
    configuration = Configuration()
    configuration.api_key['authorization'] = os.getenv('CLASH_ROYALE_API_KEY')
    locations_api = LocationsApi(ApiClient(configuration))
    clans_api = ClansApi(ApiClient(configuration))
    players_api = PlayersApi(ApiClient(configuration))

    locations = locations_api.get_locations()
    for location in locations.items:
        try:
            ranking = locations_api.get_player_ranking(location.id)
        except ApiException:
            continue
        for rank in ranking.items:
            try:
                members = clans_api.get_clan_members(rank.tag)
            except ApiException:
                continue
            for member in members.items:
                battles = players_api.get_player_battles(member.tag)
                for battle in battles:
                    if validate_battle(battle.team, battle.opponent):
                        team_deck_hash = put_cards(deck_dict, battle.team[0].cards)
                        team_crowns = default_if_none(battle.team[0].crowns, 0)
                        opponent_deck_hash = put_cards(deck_dict, battle.opponent[0].cards)
                        opponent_crowns = default_if_none(battle.opponent[0].crowns, 0)
                        if team_crowns > opponent_crowns:
                            increment_dict(win_dict, team_deck_hash, loose_dict, opponent_deck_hash)
                        elif opponent_crowns > team_crowns:
                            increment_dict(win_dict, opponent_deck_hash, loose_dict, team_deck_hash)
    return deck_dict, win_dict, loose_dict


def increment_dict(win_dict, win_deck_hash, loose_dict, loose_deck_hash):
    win_number = win_dict.get(win_deck_hash, 0)
    win_dict[win_deck_hash] = win_number + 1
    loose_number = loose_dict.get(loose_deck_hash, 0)
    loose_dict[loose_deck_hash] = loose_number + 1


def put_cards(deck_dict, cards):
    cards_name = list(map(lambda i: i.name, cards))
    deck_hash = get_hash(cards_name)
    deck_dict[deck_hash] = cards_name
    return deck_hash


def default_if_none(obj, default_value):
    return default_value if obj is None else obj


def validate_battle(team, opponent):
    if len(team) != 1 or len(opponent) != 1:
        return False
    if len(team[0].cards) != CARD_NUMBER or len(opponent[0].cards) != CARD_NUMBER:
        return False
    return True


def has_sufficient_data(dictionary, key):
    return dictionary.get(key) and dictionary[key] > SUFFICIENT_DATA
