from collections import Counter
from script import simulation_processor as sm


def need_sync(current_deck, current_relics, master_deck, master_relics) -> bool:
    return not (Counter(current_deck) == Counter(master_deck) and Counter(current_relics) == Counter(master_relics))


def create_mismatch_data(current_deck, current_relics, master_deck, master_relics) -> dict:
    """
    원본 - 전처리 데이터 간의 차이점을 추출
    임의로 sort하여 전달하면 안됨!!!!! -> 기존 run의 순서를 알아야함!
    """

    upgrade_targets, transform_targets, purge_targets, add_targets = mismatch_card_classification(current_deck, master_deck)
    relic_difference = mismatch_relics(current_relics, master_relics)

    return {
        "upgrade": upgrade_targets,
        "transform": transform_targets,
        "purge": purge_targets,
        "add": add_targets,
        "relic": relic_difference
    }


def mismatch_card_classification(current_deck, master_deck) -> tuple[list, list, list, list]:
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
    only_in_current = list((_upgraded_count - master_count).elements())

    transform_targets = list(zip(only_in_current, only_in_master))
    purge_targets = only_in_current[len(only_in_master):]
    add_targets = only_in_master[len(only_in_current):]

    return upgrade_targets, transform_targets, purge_targets, add_targets


def mismatch_relics(current_relic, master_relic):
    master_count = Counter(master_relic)
    current_count = Counter(current_relic)

    return list((master_count - current_count).elements())

