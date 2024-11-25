import json
import logging
import sts_static

# process_event 작성, process neow 나머지 분기 대응
# 원인불명의 카드강화, 유물출처를 기록하고 사후 적용해야함.

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG,
    datefmt='%m/%d/%Y %I:%M:%S',
)


def process_run(run):
    if is_corrupted_run(run):
        logging.debug(f'I found corrupted run! id: {run.get('play_id')}')

    relics = get_floorwise_relics(run)
    campfires = get_floorwise_data('campfire_choices', run)
    battles = get_floorwise_data('damage_taken', run)
    cards = get_floorwise_data('card_choices', run)
    events = get_floorwise_data('event_choices', run)
    purchases = get_floorwise_data_by_list('item_purchase_floors', run)
    purges = get_floorwise_data_by_list('items_purged_floors', run)

    print(f'''
    campfire: {campfires}
    relics: {relics}
    battle: {battles}
    card: {cards}
    event: {events}
    ''')

    current_deck = get_basic_deck(run)
    current_relics = get_basic_relic(run)
    process_neow_event(current_relics, run)

    print(f'''
    starting deck = {current_deck}
    starting relics = {current_relics}
    ''')

    battles_log = list()
    floor_reached = int(run.get('floor_reached'))

    for current_floor in range(1, floor_reached + 1):
        if current_floor in battles.keys():
            single_battle_summary = process_battle(run, current_deck, current_relics, battles[current_floor], current_floor)
            battles_log.append(single_battle_summary)
        if current_floor in cards.keys():
            process_card_choice(current_deck, current_relics, cards[current_floor])
        if current_floor in relics.keys():
            obtain_relic(current_relics, relics[current_floor].get('key'))
        if current_floor in campfires.keys():
            process_campfire(current_deck, campfires[current_floor])
        if current_floor in events.keys():
            process_event(current_deck, current_relics, events[current_floor])
        if current_floor in purchases:
            process_item_purchase(current_deck, current_relics, current_floor, run)
        if current_floor in purges:
            process_item_purge(current_deck, current_floor, run)

    print(battles_log)
    print(f'''
    original deck: {sorted(run.get('master_deck'))}
    original relics: {sorted(run.get('relics'))}
    
    processed deck: {sorted(current_deck)}
    processed relics: {sorted(current_relics)}
    ''')


# 전투 요약
def process_battle(run, current_deck, current_relics, current_battle, current_floor) -> dict:
    max_hp_list = run.get('max_hp_per_floor')
    current_hp_list = run.get('current_hp_per_floor')
    potion_used_list = run.get('potions_floor_usage')
    ascension = run.get('ascension_level')
    character = run.get('character_chosen')

    return {
        'ascension': ascension,
        'character': character,
        'floor': current_floor,
        'deck': current_deck,
        'relics': current_relics,
        'enemy': current_battle['enemies'],
        'damage_taken': int(current_battle['damage']),
        'max_hp': max_hp_list[current_floor - 1],
        'entering_hp': current_hp_list[current_floor - 1],
        'potion_used': current_floor in potion_used_list,
    }


# '?' 이벤트
def process_event(current_deck, current_relics, event):
    if 'cards_obtained' in event:
        current_deck.extend(event['cards_obtained'])
    if 'cards_removed' in event:
        for target_card in event['cards_removed']:
            current_deck.remove(target_card)
    if 'cards_upgraded' in event:
        for target_card in event['cards_upgraded']:
            smith_card(current_deck, target_card)
    if 'relics_lost' in event:
        current_relics.remove(event['relics_lost'])
    if 'relics_obtained' in event:
        current_relics.extend(event['relics_obtained'])
    if event['event_name'] == 'Vampires':
        current_relics.remove('Blood Vial')
        current_deck[:] = [card for card in current_deck if not card.startswith('Strike')]
        current_deck.extend(['Bite', 'Bite', 'Bite', 'Bite', 'Bite'])


# 카드 선택이벤트
def process_card_choice(current_deck, current_relics, card_event):
    # 카드선택 이벤트가 스킵 또는 노래하는 그릇(Singing Bowl)일 경우, 카드추가 X
    if card_event['picked'] == 'SKIP' or card_event['picked'] == 'Singing Bowl':
        return

    # 알 시리즈('Molten Egg', 'Frozen Egg', 'Toxic Egg') 업그레이드 적용
    picked_card = card_event['picked']
    is_upgraded = '+1' in picked_card
    if 'Molten Egg 2' in current_relics and picked_card in sts_static.BASE_ATTACK_CARD and ~is_upgraded:
        picked_card = picked_card + '+1'
    elif 'Frozen Egg 2' in current_relics and picked_card in sts_static.BASE_POWER_CARD and ~is_upgraded:
        picked_card = picked_card + '+1'
    elif 'Toxic Egg 2' in current_relics and picked_card in sts_static.BASE_SKILL_CARD and ~is_upgraded:
        picked_card = picked_card + '+1'

    current_deck.append(picked_card)


# 카드 강화
def smith_card(current_deck, target_card):
    smith_card_index = current_deck.index(target_card)

    # 이미 업그레이드된 카드일 경우 기존강화 +1 -> Only for 'Searing Blow'
    if '+' in current_deck[smith_card_index]:
        card_name = current_deck[smith_card_index].rsplit('+')[0]
        upgrade_count = int(current_deck[smith_card_index].rsplit('+')[1]) + 1

        current_deck[smith_card_index] = f'{card_name}+{upgrade_count}'
    else:
        current_deck[smith_card_index] += '+1'


# 불 이벤트 
def process_campfire(current_deck, campfire_event):
    event = campfire_event['key']
    if event == 'SMITH':
        smith_card(current_deck, campfire_event['data'])
    elif event == 'PURGE':
        current_deck.remove(campfire_event['data'])


# 0층 니오우 보너스
def process_neow_event(current_relics, run):
    neow_bonus = run.get('neow_bonus')
    master_relics = run.get('relics')
    if neow_bonus == 'ONE_RARE_RELIC' or neow_bonus == 'RANDOM_COMMON_RELIC':
        current_relics.append(master_relics[1])
    if neow_bonus == 'BOSS_RELIC':
        current_relics[0] = master_relics[0]
    if neow_bonus == 'THREE_ENEMY_KILL':
        current_relics.append('NeowsBlessing')
    # 'UPGRADE_CARD', 'REMOVE_CARD', 'REMOVE_TWO','TRANSFORM_CARD', 'THREE_CARDS', 'THREE_RARE_CARDS','ONE_RANDOM_RARE_CARD'
    # TODO(나머지 NEOW 이벤트에 대해서 작성해야함.)


# 상점 카드제거 
def process_item_purge(current_deck, current_floor, run):
    purge_list = run.get('items_purged')  # 제거된 카드 리스트
    purge_floor_list = run.get('items_purged_floors')  # 제거된 층 리스트

    if current_floor not in purge_floor_list:
        logging.debug(f'Current floor is not included in the purge target: {current_floor} floor, id:{run.get('play_id')}')
        return

    purge_card = purge_list[purge_floor_list.index(current_floor)]
    current_deck.remove(purge_card)


# 아이템 구매
def process_item_purchase(current_deck, current_relics, current_floor, run):
    purchase_list = run.get('items_purchased')
    purchase_floor_list = run.get('item_purchase_floors')

    if current_floor not in purchase_floor_list:
        logging.debug(f'Current floor is not included in the purchase target: {current_floor} floor, id:{run.get('play_id')}')
        return

    purchase_item_index = [i for i, value in enumerate(purchase_floor_list) if value == current_floor]
    purchase_items = [purchase_list[i] for i in purchase_item_index]

    for purchase_item in purchase_items:
        if purchase_item in sts_static.ALL_CARDS:
            current_deck.append(purchase_item)
        elif purchase_item in sts_static.ALL_RELICS:
            obtain_relic(current_relics, purchase_item)


# 유물 획득 제어
def obtain_relic(current_relics, obtained_relic):
    if obtained_relic == 'Black Blood':
        current_relics.remove('Burning Blood')
        current_relics.append('Black Blood')
        return
    elif obtained_relic == 'Ring of the Serpent':
        current_relics.remove('Ring of the Snake')
        current_relics.append('Ring of the Serpent')
        return
    elif obtained_relic == 'Frozen Core':
        current_relics.remove('Cracked Core')
        current_relics.append('Frozen Core')
        return
    elif obtained_relic == 'Holy Water':
        current_relics.remove('Pure Water')
        current_relics.append('Holy Water')
        return

    current_relics.append(obtained_relic)


# 층별 이벤트를 dict로 변환하여 제공
def get_floorwise_data(key, run) -> dict:
    data = dict()
    if key not in run:
        return data

    # floor를 key로, 나머지 성분을 value로 변환
    for attribute in run[key]:
        floor = attribute['floor']
        attribute.pop('floor')
        data[int(floor)] = attribute

    return data


def get_floorwise_data_by_list(key, run) -> list:
    return run.get(key)


# 보스유물을 포함한 유물 dict를 반환
def get_floorwise_relics(run) -> dict:
    relics = get_floorwise_data('relics_obtained', run)
    boss_relics = run.get('boss_relics')
    if len(boss_relics) >= 1:
        relics[17] = {'key': boss_relics[0]['picked']}
    if len(boss_relics) == 2:
        relics[34] = {'key': boss_relics[1]['picked']}

    return relics


# 기본덱 생성
def get_basic_deck(run) -> list:
    character = run.get('character_chosen')

    # 직업 공통 Strike 4장, Defend 4장
    deck = ['Strike', 'Strike', 'Strike', 'Strike', 'Defend', 'Defend', 'Defend', 'Defend']

    # 직업별 기본카드 기본덱에 추가
    if character == 'IRONCLAD':
        deck.extend(['Strike', 'Bash'])
        add_character_suffix(deck, '_R')
    elif character == 'THE_SILENT':
        deck.extend(['Strike', 'Defend', 'Survivor', 'Neutralize'])
        add_character_suffix(deck, '_G')
    elif character == 'DEFECT':
        deck.extend(['Dualcast', 'Zap'])
        add_character_suffix(deck, '_B')
    elif character == 'WATCHER':
        deck.extend(['Eruption', 'Vigilance'])
        add_character_suffix(deck, '_P')
    else:
        logging.debug(f'Unsupported character: {character}')
        deck = None

    # 10승천 이상 '등반자의 골칫거리' 저주카드 추가
    if 'ascension_level' in run and run.get('ascension_level') >= 10:
        deck.append('AscendersBane')

    return deck


# Strike, Defend suffix 추가
def add_character_suffix(deck, suffix):
    for index, card in enumerate(deck):
        if card == 'Strike' or card == 'Defend':
            deck[index] = card + suffix


# 기본 유물 생성
def get_basic_relic(run) -> list:
    character = run.get('character_chosen')

    if character == 'IRONCLAD':
        return ['Burning Blood']
    elif character == 'THE_SILENT':
        return ['Ring of the Snake']
    elif character == 'DEFECT':
        return ['Cracked Core']
    elif character == 'WATCHER':
        return ['PureWater']
    else:
        logging.debug(f'Unsupported character: {character}')


# 손상된, Lazy 데이터 확인
def is_corrupted_run(run) -> (bool, str):
    # 필수 필드 누락
    necessary_fields = ['boss_relics', 'campfire_choices', 'card_choices', 'character_chosen', 'damage_taken', 'event_choices', 'floor_reached',
                        'item_purchase_floors', 'items_purchased', 'items_purged', 'items_purged_floors', 'master_deck', 'relics', 'relics_obtained']
    for field in necessary_fields:
        if field not in run:
            return True

    # 시드플레이 제외
    if 'chose_seed' not in run or run.get('chose_seed') is True:
        return True

    # 최종점수 10점 이하 제외
    if 'score' not in run or run.get('score') < 10:
        return True


# run: 단일 json 플레이로그
# data: run을 1개이상 담고있는 json list
if __name__ == '__main__':
    print(get_basic_deck({'character_chosen': 'THE_SILENT'}))
    with open('../preprocessed/ironclad_test.json', 'r') as f:
        data = json.load(f)

    process_run(data)
