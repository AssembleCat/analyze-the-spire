import json
import os

from type import sts_static

json_list = [file for file in os.listdir("./json") if file.endswith(".json")]

total_count, card_filter, relic_filter, enemy_filter = 0, 0, 0, 0
ironclad_count, silent_count, defect_count, watcher_count = 0, 0, 0, 0

for idx, file in enumerate(json_list):
    with open(f"./json/{file}", 'r') as f:
        print(f"({idx+1}/{len(json_list)}) Filtering for {file}")
        data = json.load(f)
        total_count += len(data)
        ironclad, silent, defect, watcher = [], [], [], []
        filtered_data = []

        for battle in data:
            if any(card not in sts_static.ALL_CARDS for card in battle['deck']):
                card_filter += 1
                filtered_data.append(battle)
                continue
            if any(relic not in sts_static.ALL_RELICS for relic in battle['relics']):
                relic_filter += 1
                filtered_data.append(battle)
                continue
            if battle["enemy"] not in sts_static.ALL_ENEMY:
                enemy_filter += 1
                filtered_data.append(battle)
                continue

            if battle["character"] == "IRONCLAD":
                ironclad_count += 1
                ironclad.append(battle)
                continue
            if battle["character"] == "THE_SILENT":
                silent_count += 1
                silent.append(battle)
                continue
            if battle["character"] == "DEFECT":
                defect_count += 1
                defect.append(battle)
                continue
            if battle["character"] == "WATCHER":
                watcher_count += 1
                watcher.append(battle)
                continue

        if ironclad:
            with open(f"./clean/ironclad/ironclad_{file}", "w") as filter_file:
                json.dump(ironclad, filter_file)
        if silent:
            with open(f"./clean/silent/silent_{file}", "w") as filter_file:
                json.dump(silent, filter_file)
        if defect:
            with open(f"./clean/defect/defect_{file}", "w") as filter_file:
                json.dump(defect, filter_file)
        if watcher:
            with open(f"./clean/watcher/watcher_{file}", "w") as filter_file:
                json.dump(watcher, filter_file)
        if filtered_data:
            with open(f"./filter/filtered_{file}", "w") as filter_file:
                json.dump(filtered_data, filter_file)

battle_summary = {
    "total_count": total_count,
    "card_filter": card_filter,
    "relic_filter": relic_filter,
    "enemy_filter": enemy_filter,
    "ironclad": ironclad_count,
    "silent": silent_count,
    "defect": defect_count,
    "watcher": watcher_count
}

with open(f"./summary/character_summary.json") as f:
    json.dump(battle_summary, f)
