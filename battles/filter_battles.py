import json
import os

from type import sts_static

json_list = [file for file in os.listdir("./json") if file.endswith(".json")][:10]


total_count, card_filter, relic_filter, enemy_filter = 0, 0, 0, 0
for idx, file in enumerate(json_list):
    with open(f"./json/{file}", 'r') as f:
        print(f"({idx}/{len(json_list)}) Filtering for {file}")
        data = json.load(f)
        total_count += len(data)
        cleaned_data = []
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

            cleaned_data.append(battle)
        with open(f"./clean/cleaned_{file}", "w") as clean_file:
            json.dump(cleaned_data, clean_file)
        if filtered_data:
            with open(f"./filter/filtered_{file}", "w") as filter_file:
                json.dump(filtered_data, filter_file)
print(total_count, card_filter, relic_filter, enemy_filter)
