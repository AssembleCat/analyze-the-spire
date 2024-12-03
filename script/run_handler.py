def get_floorwise_data(key, run) -> dict:
    """층별 이벤트를 dict로 변환하여 제공"""
    data = dict()
    if key not in run:
        return data

    # floor를 key로, 나머지 성분을 value로 변환
    for attribute in run[key]:
        floor = attribute["floor"]
        value = attribute.copy()
        value.pop("floor")
        data[int(floor)] = value

    return data


def get_floorwise_data_by_list(key, run) -> list:
    return run.get(key)


def get_floorwise_relics(run) -> dict:
    """보스유물을 포함한 유물 dict를 반환"""
    relics = get_floorwise_data("relics_obtained", run)
    boss_relics = run["boss_relics"]
    if len(boss_relics) >= 1 and "picked" in boss_relics[0]:
        relics[17] = {"key": boss_relics[0]["picked"]}
    if len(boss_relics) == 2 and "picked" in boss_relics[1]:
        relics[34] = {"key": boss_relics[1]["picked"]}

    return relics


def is_corrupted_run(run):
    """
    :return 유효하지않은 데이터의 원인을 반환, 유효한 데이터는 None을 반환
    """
    # 필수 필드 누락
    necessary_fields = ["ascension_level", "boss_relics", "campfire_choices", "card_choices", "character_chosen", "current_hp_per_floor",
                        "damage_taken", "event_choices", "floor_reached", "item_purchase_floors", "items_purchased", "items_purged",
                        "items_purged_floors", "master_deck", "max_hp_per_floor", "neow_bonus", "neow_cost", "potions_floor_usage", "relics",
                        "relics_obtained"]

    for field in necessary_fields:
        if field not in run:
            return "missing_required_field"

    # 시드플레이 제외
    if "chose_seed" not in run and run["chose_seed"] is True:
        return "custom_seed_run"

    # 최종점수 10점 이하 제외
    if "score" not in run and run["score"] < 10:
        return "low_score"

    validation_rules = {
        "card_choices": {
            "fields": ["picked", "not_picked", "floor"],
            "error_message": "corrupted_card_choice"
        },
        "damage_taken": {
            "fields": ["damage", "enemies", "floor", "turns"],
            "error_message": "corrupted_battle"
        },
        "event_choices": {
            "fields": ["floor", "event_name"],
            "error_message": "corrupted_?_event"
        },
        "campfire_choices": {
            "fields": ["floor", "key"],
            "error_message": "corrupted_campfire"
        },
        "relics_obtained": {
            "fields": ["floor", "key"],
            "error_message": "corrupted_relic"
        }
    }

    # 검증 로직
    for key, rule in validation_rules.items():
        if run[key]:  # 데이터가 존재하고 빈 객체가 아닐때
            for row in run[key]:
                for field in rule["fields"]:
                    if field not in row:  # 필드 누락 확인
                        return rule["error_message"]

    # hp 리스트와 도달층수의 기록이 틀린 경우 제외
    reached = run["floor_reached"]
    hp_length = len(run["max_hp_per_floor"])
    if run["victory"]:
        if reached != hp_length and reached + 1 != hp_length:
            return "missing_hp_list"
    else:
        if reached + 1 != hp_length:
            return "missing_hp_list"

    return None
