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
    boss_relics = run.get("boss_relics")
    if len(boss_relics) >= 1:
        relics[17] = {"key": boss_relics[0]["picked"]}
    if len(boss_relics) == 2:
        relics[34] = {"key": boss_relics[1]["picked"]}

    return relics


def is_corrupted_run(run) -> bool:
    """손상된, Lazy 데이터 확인"""
    # 필수 필드 누락
    necessary_fields = ["boss_relics", "campfire_choices", "card_choices", "character_chosen", "damage_taken", "event_choices", "floor_reached",
                        "item_purchase_floors", "items_purchased", "items_purged", "items_purged_floors", "master_deck", "relics", "relics_obtained"]
    for field in necessary_fields:
        if field not in run:
            return True

    # 시드플레이 제외
    if "chose_seed" not in run or run.get("chose_seed") is True:
        return True

    # 최종점수 10점 이하 제외
    if "score" not in run or run.get("score") < 10:
        return True
