import os
import pandas as pd
import missing_data_handler as miss_handler
import preprocessor as preprocess
from datetime import datetime

json_name = ['ironclad_clear', 'ironclad_fail', 'silent_clear', 'silent_fail',
             'defect_clear', 'defect_fail', 'watcher_clear', 'watcher_fail']
drop_target_name = [
    'uid', 'ascension_level', 'build_version', 'campfire_choices', 'chose_seed', 'circlet_count',
    'current_hp_per_floor', 'event_choices', 'gold_per_floor', 'is_ascension_mode', 'is_beta', 'is_daily', 'is_endless',
    'is_prod', 'is_trial', 'item_purchase_floors', 'items_purged', 'items_purged_floors', 'local_time', 'killed_by',
    'max_hp_per_floor', 'path_per_floor', 'play_id', 'player_experience', 'playtime', 'potions_floor_spawned',
    'potions_floor_usage', 'relics_obtained', 'score', 'seed_played', 'seed_source_timestamp', 'timestamp', 'win_rate',
    'stored_at', 'character', 'normal_run', 'heart_run'
]
# card_choices - 카드 밸류를 선택하는 과정을 어떻게 처리할지 모르겠음.
# master_deck - 덱의 총 밸류를 어떻게 선택할것이냐!
temp_drop_name = ['card_choices', 'master_deck']


def get_data_target(root_path, data_type):
    raw_data_folder = os.path.join(project_root, 'data', data_type)

    folders = [f for f in os.listdir(raw_data_folder)]

    recent_folder, recent_time = None, None

    for folder in folders:
        folder_time = datetime.strptime(folder, '%Y%m%d-%H%M%S')

        if recent_folder is None or folder_time > recent_time:
            recent_time = folder_time
            recent_folder = folder

    return os.path.join(raw_data_folder, recent_folder)


project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
save_folder = os.path.join(project_root, 'data', 'processed')
target_folder = get_data_target(project_root, 'raw')

file_clear = pd.read_json(os.path.join(target_folder, 'silent_clear.json'))
file_fail = pd.read_json(os.path.join(target_folder, 'silent_fail.json'))

raw_df = pd.concat([file_clear, file_fail])
df = raw_df.drop(columns=drop_target_name + temp_drop_name, inplace=False)
before_drop, after_drop = raw_df.shape, df.shape

print(f"before: {before_drop}, after: {after_drop} you drop {before_drop[1] - after_drop[1]} features")
# 결측치 제거
df = miss_handler.replace_row(df)
processed_df = preprocess.run(df)

processed_df.to_json(os.path.join(save_folder, 'silent.json'), orient='records')
