import os
from datetime import datetime
from script import user_data_handler, summary_handler, json_handler

current_date = datetime.now().strftime('%Y%m%d-%H%M%S')
current_path = os.path.join(os.getcwd(), "data", "raw", current_date)

if not os.path.exists(current_path):
    os.makedirs(current_path, exist_ok=True)
    print(f"create folder name \"{current_date}\" in {current_path}")

user_infos, ironclad, silent, defect, watcher = user_data_handler.get_user_id()

run_map = {}

for user_info in user_infos:
    user_runs = user_data_handler.get_run(user_info.get('uid'), user_info.get('play_count'))

    for run in user_runs:
        run_summary = user_data_handler.single_run_summary(run)

        if run_summary is None:
            continue

        victory, character = run_summary

        run_key = f"{character}_{"clear" if victory else "fail"}"

        run_map.setdefault(run_key, []).append(run)

summary_path = os.path.join(current_path, "summary.txt")
with open(summary_path, "w") as file:
    total_count = ironclad + silent + defect + watcher
    total_true_count = sum(len(value) for value in run_map.values())

    summary_handler.write_summary(file, current_date, total_count, total_true_count, run_map, ironclad, silent, defect,
                                  watcher)

for key, data in run_map.items():
    json_handler.save_json(current_path, f"{key}.json", data)

print("end")
