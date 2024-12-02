from collections import Counter

from type import sts_static
from script import mismatch_handler as mh


def process_battle(run, current_deck, current_relics, current_battle, current_floor) -> dict:
    """전투 요약"""
    max_hp_list = run["max_hp_per_floor"]
    current_hp_list = run["current_hp_per_floor"]
    potion_used_list = run["potions_floor_usage"]
    ascension = run["ascension_level"]
    character = run["character_chosen"]
    max_hp = max_hp_list[current_floor - 1]
    entering_hp = current_hp_list[current_floor - 1]

    return {
        "ascension": ascension,
        "character": character,
        "floor": current_floor,
        "deck": current_deck.copy(),
        "relics": current_relics.copy(),
        "enemy": current_battle["enemies"],
        "damage_taken": int(current_battle["damage"]),
        "max_hp": max_hp,
        "entering_hp": entering_hp,
        "potion_used": current_floor in potion_used_list,
    }


def process_event(current_deck, current_relics, event, mismatch):
    """"?" 이벤트"""
    if "cards_obtained" in event:
        if type(event["cards_obtained"]) is list:
            for card in event["cards_obtained"]:
                mh.control_card_obtain(current_deck, card, mismatch)
        else:
            mh.control_card_obtain(current_deck, event["cards_obtained"], mismatch)
    if "cards_removed" in event:
        for target_card in event["cards_removed"]:
            if target_card in current_deck:
                purge_card(current_deck, target_card)
    if "cards_upgraded" in event:
        for target_card in event["cards_upgraded"]:
            smith_card(current_deck, target_card)
    if "relics_lost" in event:
        if isinstance(event["relics_lost"], list):
            current_relics[:] = [relic for relic in current_relics if relic not in event["relics_lost"]]
        else:
            current_relics.remove(event["relics_lost"])
    if "relics_obtained" in event:
        current_relics.extend(event["relics_obtained"])
    if event["event_name"] == "Vampires":
        if "Blood Vial" in current_relics:
            current_relics.remove("Blood Vial")
        current_deck[:] = [card for card in current_deck if not card.startswith("Strike")]
        current_deck.extend(["Bite", "Bite", "Bite", "Bite", "Bite"])


def process_card_choice(current_deck, current_relics, card_event, mismatch):
    """카드 선택이벤트"""
    if "picked" not in card_event:
        return

    # 카드선택 이벤트가 스킵 또는 노래하는 그릇(Singing Bowl)일 경우, 카드추가 X
    if card_event["picked"] == "SKIP" or card_event["picked"] == "Singing Bowl":
        return

    # 알 시리즈("Molten Egg", "Frozen Egg", "Toxic Egg") 업그레이드 적용
    picked_card = card_event["picked"]
    is_upgraded = "+1" in picked_card
    if "Molten Egg 2" in current_relics and picked_card in sts_static.BASE_ATTACK_CARD and ~is_upgraded:
        picked_card = picked_card + "+1"
    elif "Frozen Egg 2" in current_relics and picked_card in sts_static.BASE_POWER_CARD and ~is_upgraded:
        picked_card = picked_card + "+1"
    elif "Toxic Egg 2" in current_relics and picked_card in sts_static.BASE_SKILL_CARD and ~is_upgraded:
        picked_card = picked_card + "+1"

    mh.control_card_obtain(current_deck, picked_card, mismatch)


def smith_card(current_deck, target_card):
    """카드 강화"""
    if target_card not in current_deck:
        return

    smith_card_index = current_deck.index(target_card)

    current_deck[smith_card_index] = get_upgraded_card(current_deck[smith_card_index])


def purge_card(current_deck, target_card):
    if target_card not in current_deck:
        return

    current_deck.remove(target_card)


# 이미 업그레이드된 카드일 경우 기존강화 +1 -> Only for "Searing Blow"
def get_upgraded_card(card):
    if "+" in card:
        card_name = card.rsplit("+")[0]
        upgrade_count = int(card.rsplit("+")[1]) + 1

        return f"{card_name}+{upgrade_count}"
    else:
        return card + "+1"


def process_campfire(current_deck, campfire_event):
    """불 이벤트"""
    event = campfire_event["key"]
    if event == "SMITH":
        if type(campfire_event["data"]) is list:
            for card in campfire_event["data"]:
                smith_card(current_deck, card)
        else:
            smith_card(current_deck, campfire_event["data"])
    elif event == "PURGE":
        purge_card(current_deck, campfire_event["data"])


def process_neow_event(current_relics, run):
    """0층 니오우 보너스, 페널티"""
    neow_bonus = run["neow_bonus"]
    neow_cost = run["neow_cost"]
    master_relics = run["relics"]

    if neow_bonus == "ONE_RARE_RELIC" or neow_bonus == "RANDOM_COMMON_RELIC":
        current_relics.append(master_relics[1])
    if neow_bonus == "BOSS_RELIC":
        current_relics[0] = master_relics[0]
    if neow_bonus == "THREE_ENEMY_KILL":
        current_relics.append("NeowsBlessing")


def process_item_purge(current_deck, current_floor, run):
    purge_list = run.get("items_purged")  # 제거된 카드 리스트
    purge_floor_list = run.get("items_purged_floors")  # 제거된 층 리스트

    purge_item_index = [i for i, value in enumerate(purge_floor_list) if value == current_floor]
    purge_items = [purge_list[i] for i in purge_item_index]

    for purge_item in purge_items:
        if purge_item in current_deck:
            purge_target_card = purge_list[purge_floor_list.index(current_floor)]
            purge_card(current_deck, purge_target_card)


def process_item_purchase(current_deck, current_relics, current_floor, run, mismatch):
    """아이템 구매"""
    purchase_list = run.get("items_purchased")
    purchase_floor_list = run.get("item_purchase_floors")

    purchase_item_index = [i for i, value in enumerate(purchase_floor_list) if value == current_floor]
    purchase_items = [purchase_list[i] for i in purchase_item_index]

    for purchase_item in purchase_items:
        if purchase_item in sts_static.ALL_CARDS:
            current_deck.append(purchase_item)
        elif purchase_item in sts_static.ALL_RELICS:
            obtain_relic(current_deck, current_relics, purchase_item, mismatch)


def process_card_transform(current_deck, transform_summary):
    original, target = transform_summary
    card_idx = current_deck.index[original]
    current_deck[card_idx] = target


def process_card_add(current_deck, add_cards):
    current_deck.extend(add_cards)


def process_relic(current_deck, current_relics, obtained_relic, mismatch):
    if type(obtained_relic) is list:
        for relic in obtained_relic:
            obtain_relic(current_deck, current_relics, relic, mismatch)
    else:
        obtain_relic(current_deck, current_relics, obtained_relic, mismatch)


def obtain_relic(current_deck, current_relics, obtained_relic, mismatch):
    """유물 획득 제어"""
    if obtained_relic == "Black Blood":
        current_relics.remove("Burning Blood")
        current_relics.append("Black Blood")
        return
    elif obtained_relic == "Ring of the Serpent":
        current_relics.remove("Ring of the Snake")
        current_relics.append("Ring of the Serpent")
        return
    elif obtained_relic == "Frozen Core":
        current_relics.remove("Cracked Core")
        current_relics.append("Frozen Core")
        return
    elif obtained_relic == "Holy Water":
        current_relics.remove("Pure Water")
        current_relics.append("Holy Water")
        return

    if obtained_relic == "Empty Cage" and mismatch["purge"]:
        for target_card in mismatch["purge"][:2]:
            purge_card(current_deck, target_card)
    if obtained_relic == "War Paint" and mismatch["upgrade"]:
        attack_card = [card for card in mismatch["upgrade"] if card_type(card) == "attack"][:2]
        for card in attack_card:
            mismatch["upgrade"].remove(card)
            smith_card(current_deck, card)
    if obtained_relic == "Whetstone" and mismatch["upgrade"]:
        skill_card = [card for card in mismatch["upgrade"] if card_type(card) == "skill"][:2]
        for card in skill_card:
            mismatch["upgrade"].remove(card)
            smith_card(current_deck, card)
    if obtained_relic == "Calling Bell" and mismatch["relic"]:
        current_relics.extend(mismatch["relic"])
        current_deck.append("CurseOfTheBell")

    current_relics.append(obtained_relic)


def card_type(card):
    if card in sts_static.BASE_SKILL_CARD:
        return "skill"
    if card in sts_static.BASE_ATTACK_CARD:
        return "attack"
    if card in sts_static.BASE_POWER_CARD:
        return "power"
    if card in sts_static.BASE_CURSE_CARD:
        return "curse"

    raise Exception(f"unknown card found: {card}")


if __name__ == "__main__":
    master = ['Attack_R', 'Defend_R', 'Defend_R', 'Defend_R', 'Feel No Pain', 'Fiend Fire+1', 'Fiend Fire+1', 'Flame Barrier', 'Ghostly Armor',
              'Power Through+1',
              'Feel No Pain+1']
    current = ['Defend_R', 'Defend_R', 'Defend_R', 'Defend_R', 'Feel No Pain', 'Fiend Fire', 'Fiend Fire', 'Flame Barrier', 'Ghostly Armor',
               'Power Through', 'Feel No Pain']
