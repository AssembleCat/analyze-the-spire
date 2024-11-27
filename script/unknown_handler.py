from collections import Counter
from script import simulation_processor as sm


def sync_unknown_data(current_deck, current_relics, master_deck, master_relics, run, unknowns):
    """
    원본 - 전처리 데이터 간의 차이점을 채우기 위한 함수
    임의로 sort하여 전달하면 안됨!!!!! -> 기존 run의 순서를 알아야함!
    """

    upgrade_targets, transform_targets, purge_targets, add_targets = unknown_card_classification(current_deck, master_deck)

    # 강화
    if len(upgrade_targets) > 0:
        upgrade_summary = unknown_upgrade_classification(upgrade_targets, unknowns["upgrade"])
        for floor, current_upgrade_target in upgrade_summary.items():
            run["campfire_choices"] = {"floor": floor, "data": current_upgrade_target, "key": "SMITH"}
    # 변환
    if len(transform_targets) > 0:
        run["card_transform"] = unknown_transform_classification(transform_targets, unknowns["transform"])
    # 제거
    if len(purge_targets) > 0:
        for floor, purge_count in unknowns["purge"].items():
            current_purge_target = find_purge_target_for_current_floor(purge_targets, purge_count)
            run["items_purged_floors"].extend([floor] * purge_count)
            run["items_purged"].extend(current_purge_target)
    # 추가
    if len(add_targets) > 0:
        for floor, add_type in unknowns["add"].items():
            print('')
    # 유물
    if "relic" in unknowns.keys():
        relic_target = list((Counter(master_relics) - Counter(current_relics)).elements())
        for floor, relic_count in unknowns["relic"].items():
            current_relic_target = find_relics_for_current_floor(relic_target, relic_count)
            run["relics_obtained"] = {"floor": floor, "key": current_relic_target}

    return run


def unknown_card_classification(current_deck, master_deck):
    master_count = Counter(master_deck)
    current_count = Counter(current_deck)

    # 업그레이드 대상
    upgrade_targets = []

    for card, count in master_count.items():
        if '+' in card:
            base_card = card.rsplit('+')[0]
            if base_card in current_count:
                downgraded_count = min(count, current_count[base_card])
                upgrade_targets.extend([base_card] * downgraded_count)

    _upgraded_deck = current_deck.copy()

    # 임시로 전처리덱 강화
    for card in upgrade_targets:
        sm.smith_card(_upgraded_deck, card)

    _upgraded_count = Counter(_upgraded_deck)

    # 각 덱에만 존재하는 카드
    only_in_master = list((master_count - _upgraded_count).elements())
    only_in_current = list((_upgraded_deck - master_count).elements())

    transform_targets = list(zip(only_in_current, only_in_master))
    purge_targets = only_in_current[len(only_in_master):]
    add_targets = only_in_master[len(only_in_current):]

    return upgrade_targets, transform_targets, purge_targets, add_targets


def unknown_upgrade_classification(upgrade_target, unknown_upgrade) -> dict:
    """
    upgrade_target: 강화가 필요한 카드 리스트
    unknown_upgrade: unknown의 강화해야할 카드 타입("skill", "attack", "power")
    """
    upgrade_summary = {}

    for floor, card_types in unknown_upgrade.items():
        upgrade_summary[floor] = upgrade_target[:len(card_types)]
        del upgrade_target[:len(card_types)]

    return upgrade_summary


def unknown_transform_classification(transform_targets, unknown_transform) -> list:
    transform_summary = []

    for floor, trans_count in unknown_transform.items():
        current_transform_card = transform_targets[:trans_count]
        del transform_targets[:trans_count]
        original, target = current_transform_card.keys(), current_transform_card.values()
        transform_summary.append({"floor": floor, "original": original,  "target": target})

    return transform_summary


def find_purge_target_for_current_floor(purge_target, purge_count):
    current_purge_target = purge_target[:purge_count]
    del purge_target[:purge_count]

    return current_purge_target


def find_relics_for_current_floor(relics, relic_count):
    current_relics = relics[:relic_count]
    del relics[:relic_count]

    return current_relics
