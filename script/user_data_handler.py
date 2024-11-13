import os
import requests
from type import Character
from script import json_handler

server_url = "https://zibodphuevointzxjook.supabase.co"
headers = {
    'ApiKey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppYm9kcGh1ZXZvaW50enhqb29rIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NDkwNTA0NzksImV4cCI6MTk2NDYyNjQ3OX0.rJJdqAOIEd50s9ajIm97FGnDfMtRCvU_H9VMmxub_yk'
}


def get_user_id(start=1, end=200):
    user_infos = []
    ironclad, silent, defect, watcher = 0, 0, 0, 0

    for user_id in range(start, end):
        response = requests.get(f'{server_url}/rest/v1/players?select=*&id=eq.{user_id}',
                                headers=headers).json()

        # 공백 검사
        if str(response) == "[]":
            continue

        play_count = response[0].get('total_play_counts')

        # 플레이 기록 없으면 제외
        if play_count is None:
            continue

        ironclad += int(play_count.get('ironclad'))
        silent += int(play_count.get('silent'))
        defect += int(play_count.get('defect'))
        watcher += int(play_count.get('watcher'))

        user_infos.append({"play_count": play_count, "uid": response[0].get('uid')})

    return user_infos, ironclad, silent, defect, watcher


def get_run(user_id, play_count):
    total_play_count = play_count.get('ironclad') + play_count.get('silent') + play_count.get(
        'defect') + play_count.get('watcher')
    all_runs = []
    offset = 0
    request_size = 1000

    while offset < total_play_count:
        response = requests.get(
            f'{server_url}/rest/v1/stored_runs?select=*&uid=eq.{user_id}&offset={offset}',
            headers=headers).json()

        all_runs.extend(response)
        offset += request_size

    print(f"user: {user_id} have {len(all_runs)} runs")

    return all_runs


# 단일 run에 대한 정보 확인
def single_run_summary(run):
    victory, character = False, None

    # 15승천 미만, 옛날 빌드버전, 일일도전, 시드플레이 제외
    if run.get('ascension_level') < 15:
        return None

    # if run.get('build_version') != '2022-12-18':
    #     return None

    if run.get('is_daily') or run.get('chose_seed'):
        return None

    character = Character.get_character_type(run.get('character'))
    if character is None:
        return None

    victory = run.get('victory')

    return victory, character


def save_run(path, file_name, data):
    full_path = os.path.join(path, file_name)

    if os.path.exists(full_path):
        json_handler.append_json_file(full_path, data)
    else:
        json_handler.create_json_file(full_path, data)
