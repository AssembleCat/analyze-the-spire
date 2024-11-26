from type import sts_static

# 전투 요약
def process_battle(run, current_deck, current_relics, current_battle, current_floor) -> dict:
    max_hp_list = run.get("max_hp_per_floor")
    current_hp_list = run.get("current_hp_per_floor")
    potion_used_list = run.get("potions_floor_usage")
    ascension = run.get("ascension_level")
    character = run.get("character_chosen")
    max_hp = max_hp_list[0] if current_floor is 1 else max_hp_list[current_floor - 2]
    entering_hp = current_hp_list[0] if current_floor is 1 else current_hp_list[current_floor - 2]

    return {
        "ascension": ascension,
        "character": character,
        "floor": current_floor,
        "deck": current_deck.copy(),
        "relics": current_relics.copy(),
        "enemy": current_battle["enemies"],
        "damage_taken": int(current_battle["damage"]),
        "max_hp": max_hp,
        "entering_hp": current_hp_list[current_floor - 2],
        "potion_used": current_floor in potion_used_list,
    }


# "?" 이벤트
def process_event(current_deck, current_relics, event):
    if "cards_obtained" in event:
        current_deck.extend(event["cards_obtained"])
    if "cards_removed" in event:
        for target_card in event["cards_removed"]:
            current_deck.remove(target_card)
    if "cards_upgraded" in event:
        for target_card in event["cards_upgraded"]:
            smith_card(current_deck, target_card)
    if "relics_lost" in event:
        current_relics.remove(event["relics_lost"])
    if "relics_obtained" in event:
        current_relics.extend(event["relics_obtained"])
    if event["event_name"] == "Vampires":
        current_relics.remove("Blood Vial")
        current_deck[:] = [card for card in current_deck if not card.startswith("Strike")]
        current_deck.extend(["Bite", "Bite", "Bite", "Bite", "Bite"])


# 카드 선택이벤트
def process_card_choice(current_deck, current_relics, card_event):
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

    current_deck.append(picked_card)


# 카드 강화
def smith_card(current_deck, target_card):
    smith_card_index = current_deck.index(target_card)

    # 이미 업그레이드된 카드일 경우 기존강화 +1 -> Only for "Searing Blow"
    if "+" in current_deck[smith_card_index]:
        card_name = current_deck[smith_card_index].rsplit("+")[0]
        upgrade_count = int(current_deck[smith_card_index].rsplit("+")[1]) + 1

        current_deck[smith_card_index] = f"{card_name}+{upgrade_count}"
    else:
        current_deck[smith_card_index] += "+1"


# 불 이벤트
def process_campfire(current_deck, campfire_event):
    event = campfire_event["key"]
    if event == "SMITH":
        smith_card(current_deck, campfire_event["data"])
    elif event == "PURGE":
        current_deck.remove(campfire_event["data"])


# 0층 니오우 보너스
def process_neow_event(current_relics, run, unknowns):
    neow_bonus = run.get("neow_bonus")
    master_relics = run.get("relics")
    if neow_bonus == "ONE_RARE_RELIC" or neow_bonus == "RANDOM_COMMON_RELIC":
        current_relics.append(master_relics[1])
    if neow_bonus == "BOSS_RELIC":
        current_relics[0] = master_relics[0]
    if neow_bonus == "THREE_ENEMY_KILL":
        current_relics.append("NeowsBlessing")
    if neow_bonus == "REMOVE_CARD":
        unknowns["purge"].append({0: 1})
    if neow_bonus == "REMOVE_TWO":
        unknowns["purge"].append({0: 2})
    if neow_bonus == "UPGRADE_CARD":
        unknowns["upgrade"] = {{0: ["unknown"]}}  # tlqkf 이거 어캐하냐 뭘 업글했는지 어캐알아 ㅋㅋ
    # "UPGRADE_CARD","TRANSFORM_CARD", "THREE_CARDS", "THREE_RARE_CARDS","ONE_RANDOM_RARE_CARD"
    # TODO(나머지 NEOW 이벤트에 대해서 작성해야함.)


def process_item_purge(current_deck, current_floor, run):
    purge_list = run.get("items_purged")  # 제거된 카드 리스트
    purge_floor_list = run.get("items_purged_floors")  # 제거된 층 리스트

    purge_item_index = [i for i, value in enumerate(purge_floor_list) if value == current_floor]
    purge_items = [purge_list[i] for i in purge_item_index]

    for purge_item in purge_items:
        purge_card = purge_list[purge_floor_list.index(current_floor)]
        current_deck.remove(purge_card)


# 아이템 구매
def process_item_purchase(current_deck, current_relics, current_floor, run, unknowns):
    purchase_list = run.get("items_purchased")
    purchase_floor_list = run.get("item_purchase_floors")

    purchase_item_index = [i for i, value in enumerate(purchase_floor_list) if value == current_floor]
    purchase_items = [purchase_list[i] for i in purchase_item_index]

    for purchase_item in purchase_items:
        if purchase_item in sts_static.ALL_CARDS:
            current_deck.append(purchase_item)
        elif purchase_item in sts_static.ALL_RELICS:
            obtain_relic(current_deck, current_relics, current_floor, purchase_item, unknowns)


# 유물 획득 제어
def obtain_relic(current_deck, current_relics, current_floor, obtained_relic, unknowns):
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

    if obtained_relic == "Empty Cage":
        unknowns["purge"] = {current_floor: 2}
    if obtained_relic == "War Paint":
        unknowns.setdefault("upgrade", {}).setdefault(current_floor, [])
        unknowns["upgrade"][current_floor].extend(["skill", "skill"])
    if obtained_relic == "Whetstone":
        unknowns.setdefault("upgrade", {}).setdefault(current_floor, [])
        unknowns["upgrade"][current_floor].extend(["attack", "attack"])
    if obtained_relic == "Calling Bell":
        current_relics.extend(["TEMP_RELIC", "TEMP_RELIC", "TEMP_RELIC"])
        current_deck.append("CurseOfTheBell")

    current_relics.append(obtained_relic)


# 원본 - 전처리 데이터 간의 차이점을 채우기 위한 함수
# 임의로 sort하여 전달하면 안됨!!!!! -> 기존 run의 순서를 알아야함!
def sync_unknown_data(current_deck, current_relics, master_deck, master_relics, run, unknowns):
    # 강화
    if "upgrade" in unknowns.keys():
        upgrade_target = find_upgrade_target(current_deck, master_deck)
        for floor, upgrade_list in unknowns["upgrade"].items():
            current_upgrade_target = find_upgrade_target_for_current_floor(upgrade_target, upgrade_list)
            # TODO(기존 층의 강화정보를 덮어 씌울 가능성이 있는지 점검 + extend를 고려해야함.)
            run["campfire_choices"].append({"data": current_upgrade_target, "floor": floor, "key": "SMITH"})
    # 제거대상 items_purged_floors, items_purged에 각각 추가`
    # 유물 리스트에 TEMP_RELIC이 들어있으면 원본 유물과 비교하여 boss_relic이 'Calling Bell'인 시점에 유물 추가 relics_obtained { "floor": 획득 층, "key": "MealTicket" }

    return run


# 원본/전처리 덱 간의 차이점으로 업그레이드가 필요한 카드 추출
def find_upgrade_target(current_deck, master_deck):
    master_count = Counter(master_deck)
    current_count = Counter(current_deck)

    upgrade_target_cards = []

    for card, count in master_count.items():
        if '+' in card:
            base_card = card.rsplit('+')[0]
            if base_card in current_count:
                downgraded_count = min(count, current_count[base_card])
                upgrade_target_cards.extend([card] * downgraded_count)

    return upgrade_target_cards


def find_upgrade_target_for_current_floor(upgrade_target, current_upgrade_type):
    """
    upgrade_target: 강화가 필요한 카드 리스트
    current_upgrade_type: 현재 층에서 강화해야할 카드 타입 리스트("skill", "attack", "power")
    """
    current_upgrade_target = []

    # 강화타입과 일치하는 대상카드를 찾음
    for current_card_type in current_upgrade_type:
        for card in upgrade_target:
            if card_type(card) == current_card_type:
                current_upgrade_target.append(card)
                break

    # 강화할 카드를 찾으면 강화대상에서 제거
    for remove_from_upgrade_target in current_upgrade_target:
        upgrade_target.remove(remove_from_upgrade_target)

    return current_upgrade_target


def card_type(card):
    if card in sts_static.BASE_SKILL_CARD:
        return "skill"
    if card in sts_static.BASE_ATTACK_CARD:
        return "attack"
    if card in sts_static.BASE_POWER_CARD:
        return "power"

    raise Exception(f"unknown card found: {card}")
