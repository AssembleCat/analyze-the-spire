import json
import logging
from script import run_handler as rh, simulation_processor as sp, mismatch_handler as mh

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=logging.DEBUG,
    datefmt="%m/%d/%Y %I:%M:%S",
)


def process_run(run, mismatch=mh.create_default_mismatch_data()):
    # 유효하지 않은 로그 제외
    if rh.is_corrupted_run(run):
        logging.debug(f"I found corrupted run! id: {run["play_id"]}")
        return

    # 이벤트, 전투, 카드, 유물 정보
    relics = rh.get_floorwise_relics(run)
    campfires = rh.get_floorwise_data("campfire_choices", run)
    battles = rh.get_floorwise_data("damage_taken", run)
    cards = rh.get_floorwise_data("card_choices", run)
    events = rh.get_floorwise_data("event_choices", run)
    purchases = rh.get_floorwise_data_by_list("item_purchase_floors", run)
    purges = rh.get_floorwise_data_by_list("items_purged_floors", run)

    # starting 덱, 유물
    current_deck = get_basic_deck(run, mismatch)
    current_relics = get_basic_relic(run)

    # 0층 이벤트, neow 적용
    sp.process_neow_event(current_relics, run)
    battles_log = list()
    floor_reached = int(run["floor_reached"])

    # 0층 ~ 마지막층별 이벤트 검사
    for current_floor in range(0, floor_reached + 1):
        if current_floor in battles.keys():
            single_battle_summary = sp.process_battle(run, current_deck, current_relics, battles[current_floor], current_floor)
            battles_log.append(single_battle_summary)
        if current_floor in campfires.keys():
            sp.process_campfire(current_deck, campfires[current_floor])
        if current_floor in cards.keys():
            sp.process_card_choice(current_deck, current_relics, cards[current_floor], mismatch)
        if current_floor in relics.keys():
            sp.process_relic(current_deck, current_relics, relics[current_floor]["key"], mismatch)
        if current_floor in events.keys():
            sp.process_event(current_deck, current_relics, events[current_floor], mismatch)
        if current_floor in purchases:
            sp.process_item_purchase(current_deck, current_relics, current_floor, run, mismatch)
        if current_floor in purges:
            sp.process_item_purge(current_deck, current_floor, run)

    # 원본/전처리 덱과 유물간에 차이가 있을경우 동기화 적용!
    if mh.need_sync(current_deck, current_relics, run["master_deck"], run["relics"]):
        mismatch = mh.create_mismatch_data(current_deck, current_relics, run["master_deck"], run["relics"])

        process_run(run, mismatch)
    else:
        print("run 저장")


def get_basic_deck(run, mismatch) -> list:
    """기본덱 생성"""
    character = run["character_chosen"]

    # 직업 공통 Strike 4장, Defend 4장
    deck = ["Strike", "Strike", "Strike", "Strike", "Defend", "Defend", "Defend", "Defend"]

    # 직업별 기본카드 기본덱에 추가
    if character == "IRONCLAD":
        deck.extend(["Strike", "Bash"])
        add_character_suffix(deck, "_R")
    elif character == "THE_SILENT":
        deck.extend(["Strike", "Defend", "Survivor", "Neutralize"])
        add_character_suffix(deck, "_G")
    elif character == "DEFECT":
        deck.extend(["Dualcast", "Zap"])
        add_character_suffix(deck, "_B")
    elif character == "WATCHER":
        deck.extend(["Eruption", "Vigilance"])
        add_character_suffix(deck, "_P")
    else:
        logging.debug(f"Unsupported character: {character}")
        deck = None

    # 10승천 이상 "등반자의 골칫거리" 저주카드 추가
    if "ascension_level" in run and run["ascension_level"] >= 10:
        deck.append("AscendersBane")

    synced_deck = []
    for card in deck:
        mh.control_card_obtain(synced_deck, card, mismatch)

    return synced_deck


def add_character_suffix(deck, suffix):
    """Strike, Defend suffix 추가"""
    for index, card in enumerate(deck):
        if card == "Strike" or card == "Defend":
            deck[index] = card + suffix


def get_basic_relic(run) -> list:
    """기본 유물 생성"""
    character = run["character_chosen"]

    if character == "IRONCLAD":
        return ["Burning Blood"]
    elif character == "THE_SILENT":
        return ["Ring of the Snake"]
    elif character == "DEFECT":
        return ["Cracked Core"]
    elif character == "WATCHER":
        return ["PureWater"]
    else:
        logging.debug(f"Unsupported character: {character}")


# run: 단일 json 플레이로그
# data: run을 1개이상 담고있는 json list
if __name__ == "__main__":
    with open("../preprocessed/ironclad_test.json", "r") as f:
        data = json.load(f)

    process_run(data)
