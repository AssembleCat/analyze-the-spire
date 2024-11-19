import os
from concurrent.futures import ProcessPoolExecutor
import datetime

from data import parquet_loader
import pandas as pd


# 파일 필터 함수
def filter_file(path):
    print(f'Filtering {path}')
    df = pd.read_parquet(path)

    removal_counts = {
        'total_count': len(df),
        'character_chosen': 0,
        'ascension_level': 0,
        'floor_reached': 0,
        'is_endless': 0,
        'is_beta': 0,
        'is_trial': 0,
        'is_daily': 0,
        'is_prod': 0,
        'after_filtered': 0
    }

    # 필터링 및 필터대상 갯수 저장
    valid_character = ['IRONCLAD', 'THE_SILENT', 'DEFECT', 'WATCHER']
    mask = (
            df['character_chosen'].isin(valid_character) &
            df['ascension_level'].between(0, 20) &
            df['floor_reached'].between(0, 57) &
            (df['is_endless'] != True) &
            (df['is_beta'] != True) &
            (df['is_trial'] != True) &
            (df['is_daily'] != True) &
            (df['is_prod'] != True)
    )

    removal_counts['after_filtered'] = mask.sum()
    removal_counts['total_count'] = len(df)
    removal_counts['character_chosen'] = len(df) - df['character_chosen'].isin(valid_character).sum()
    removal_counts['ascension_level'] = len(df) - df['ascension_level'].between(0, 20).sum()
    removal_counts['floor_reached'] = len(df) - df['floor_reached'].between(0, 57).sum()
    removal_counts['is_endless'] = len(df) - (df['is_endless'] != True).sum()
    removal_counts['is_beta'] = len(df) - (df['is_beta'] != True).sum()
    removal_counts['is_trial'] = len(df) - (df['is_trial'] != True).sum()
    removal_counts['is_daily'] = len(df) - (df['is_daily'] != True).sum()
    removal_counts['is_prod'] = len(df) - (df['is_prod'] != True).sum()

    df_filtered = df[mask]

    removal_counts['after_filtered'] = len(df_filtered)

    # 필터 데이터 저장
    save_path = str(path).replace('Compressed', 'Filtered')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df_filtered.to_parquet(save_path, engine='fastparquet')

    return removal_counts


# 결과 병합 함수
def combine_results(results):
    total_removal_counts = {
        'total_count': 0,
        'character_chosen': 0,
        'ascension_level': 0,
        'floor_reached': 0,
        'is_endless': 0,
        'is_beta': 0,
        'is_trial': 0,
        'is_daily': 0,
        'is_prod': 0,
        'after_filtered': 0
    }

    for result in results:
        for key in total_removal_counts.keys():
            total_removal_counts[key] += result[key]

    return total_removal_counts


if __name__ == '__main__':
    file_paths = parquet_loader.get_file_paths(reverse=True)
    total_files = len(file_paths)

    print(f"Start filtering {total_files} files...")

    with ProcessPoolExecutor(max_workers=4) as executor:
        result = list(executor.map(filter_file, file_paths))

    final_counts = combine_results(result)

    output_file = 'data_filtering.txt'
    with open(output_file, 'w') as f:
        f.write(f'Filtering time: {datetime.datetime.now()}\n')
        for category, count in final_counts.items():
            f.write(f'{category}: {count}\n')
