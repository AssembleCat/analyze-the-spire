import json
import logging
import os
import traceback
from collections import defaultdict

import pandas as pd
from data import parquet_loader as pl
from script import run_handler as rh, simulation_processor as sp, mismatch_handler as mh

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=logging.DEBUG,
    datefmt="%m/%d/%Y %I:%M:%S",
)


def simulate_entire_runs(data_paths):
    # 검사 파일 갯수 추적
    count, end = 0, len(data_paths)

    # 성공/실패 갯수 기록
    simulation_count = defaultdict(int)
    failed_files = []

    # 각 파일별로 실행
    for file in data_paths:
        count += 1
        logging.debug(f"({count}/{end}) Processing for {os.path.basename(file)}")
        try:
            df = pd.read_parquet(file)

            # file단위로 battle을 수집
            result_collector = list()

            # 해당 파일에 대한 count 수집
            local_simulation_count = defaultdict(int)
            local_simulation_count["total_run"] += df.shape[0]
            for index, row in df.iterrows():
                # 오염된 로그를 제외 및 원인 기록
                valid_check = rh.is_corrupted_run(row)
                if valid_check is not None:
                    local_simulation_count[valid_check] += 1
                    continue
                # 처리결과 저장
                result = process_single_run(row.to_dict())
                local_simulation_count["processed"] += 1
                result_collector.extend(result)
            # battle list 저장
            save_json(f'../battles/{os.path.basename(file)}.json', result_collector)

            # global simulation_count에 반영
            for key, value in local_simulation_count.items():
                simulation_count[key] += value

        except Exception as e:
            # 오류 발생시 실패한 리스트에 기록
            failed_files.append(file)
            logging.error(f"Error processing file {file}: from({type(e).__name__}) {e}")
            logging.error(traceback.format_exc())

    save_json("../battles/battle_summary.json", simulation_count)
    if failed_files:
        save_json("../battles/process_failed_list.json", failed_files)


def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)


def process_single_run(run, mismatch=None, recursion=False):
    """
    :param run: 단일 런 로그파일 key-value로 접근할 수 있도록 가공해야함.
    :param mismatch: 자동으로 할당되는 원본-전처리덱간의 차이점 임의로 제공하지않아야함.
    :param recursion: 현재 process가 재귀된 상태인지를 표현
    :return: 전투별 요약 리스트
    """
    if mismatch is None:
        mismatch = mh.create_default_mismatch_data()

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

    # 재귀된 process일 경우 검사없이 반환
    if recursion:
        return battles_log
    # 원본/전처리 덱과 유물간에 차이가 있을경우 동기화 적용!
    elif mh.need_sync(current_deck, current_relics, run["master_deck"], run["relics"]):
        mismatch = mh.create_mismatch_data(current_deck, current_relics, run["master_deck"], run["relics"])
        return process_single_run(run, mismatch, True)
    else:
        return battles_log


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
    # 총 384개 있음
    data_paths = pl.get_file_paths(folder_type="ClassifiedData")[:100]
    simulate_entire_runs(data_paths)

    # single sample run
    # with open("../sample/defect_test.json", "r") as f:
    #    data = json.load(f)

    # single_result = process_single_run(data)
    # with open("../sample/ironclad_test_output.json", "w") as f:
    #     json.dump(single_result, f)
