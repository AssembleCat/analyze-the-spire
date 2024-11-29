from collections import Counter
from script import simulation_processor as sp


def need_sync(current_deck, current_relics, master_deck, master_relics) -> bool:
    return Counter(current_deck) != Counter(master_deck) or Counter(current_relics) != Counter(master_relics)


def create_default_mismatch_data():
    return {
        "upgrade": [],
        "purge": [],
        "add": [],
        "relic": []
    }


def create_mismatch_data(current_deck, current_relics, master_deck, master_relics) -> dict:
    """
    원본 - 전처리 데이터 간의 차이점을 추출
    임의로 sort하여 전달하면 안됨!!!!! -> 기존 run의 순서를 알아야함!
    """

    upgrade_targets, purge_targets, add_targets = mismatch_card_classification(current_deck, master_deck)
    relic_difference = mismatch_relics(current_relics, master_relics)

    return {
        "upgrade": upgrade_targets,
        "purge": purge_targets,
        "add": add_targets,
        "relic": relic_difference
    }


def mismatch_card_classification(current_deck, master_deck) -> tuple[list, list, list]:
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
        sp.smith_card(_upgraded_deck, card)

    # 각 덱에만 존재하는 카드
    add_targets = list((master_count - Counter(_upgraded_deck)).elements())
    purge_targets = list((Counter(_upgraded_deck) - master_count).elements())

    return upgrade_targets, purge_targets, add_targets


def mismatch_relics(current_relic, master_relic):
    master_count = Counter(master_relic)
    current_count = Counter(current_relic)

    return list((master_count - current_count).elements())


def control_card_obtain(current_deck, obtained_card, mismatch):
    purge, add, upgrade = mismatch["purge"], mismatch["add"], mismatch["upgrade"]
    if obtained_card in upgrade:
        upgrade.remove(obtained_card)
        current_deck.append(sp.get_upgraded_card(obtained_card))
    elif obtained_card in purge and add:
        purge.remove(obtained_card)
        current_deck.append(add.pop(0))
    elif obtained_card in purge:
        purge.remove(obtained_card)
    else:
        current_deck.append(obtained_card)


if __name__ == '__main__':
    master = ['Attack_R', 'Defend_R', 'Defend_R', 'Defend_R', 'Feel No Pain', 'Fiend Fire+1', 'Fiend Fire+1', 'Flame Barrier', 'Ghostly Armor',
              'Power Through+1', 'Feel No Pain+1']
    current = ['Defend_R', 'Defend_R', 'Defend_R', 'Defend_R', 'Feel No Pain', 'Fiend Fire', 'Fiend Fire', 'Flame Barrier', 'Ghostly Armor',
               'Power Through', 'Feel No Pain']
