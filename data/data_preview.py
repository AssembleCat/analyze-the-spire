from concurrent.futures import ProcessPoolExecutor
from data import parquet_loader
import pandas as pd
import numpy as np
import multiprocessing


# 파일 처리 함수
def process_file(path, counter, progress_queue):
    try:
        df = pd.read_parquet(path, columns=['character_chosen', 'ascension_level', 'floor_reached', 'victory'])
        char_vals, char_counts = np.unique(df['character_chosen'].to_numpy(), return_counts=True)
        asc_vals, asc_counts = np.unique(df['ascension_level'].to_numpy(), return_counts=True)
        floor_vals, floor_counts = np.unique(df['floor_reached'].to_numpy(), return_counts=True)
        vic_vals, vic_counts = np.unique(df['victory'].to_numpy(), return_counts=True)

        counter.value += 1
        progress_queue.put(counter.value)  # 진행 상황을 큐에 추가

        return {
            'character_chosen': dict(zip(char_vals, char_counts)),
            'ascension_level': dict(zip(asc_vals, asc_counts)),
            'floor_reached': dict(zip(floor_vals, floor_counts)),
            'victory': dict(zip(vic_vals, vic_counts)),
        }
    except Exception as e:
        print(f"Error processing file {path}: {e}")
        raise


# 결과 병합 함수
def combine_results(results):
    combined = {
        'character_chosen': {},
        'ascension_level': {},
        'floor_reached': {},
        'victory': {},
    }

    for result in results:
        for key in combined.keys():
            for val, count in result[key].items():
                combined[key][val] = combined[key].get(val, 0) + count

    return combined


# 병렬 처리 실행
if __name__ == '__main__':
    file_paths = parquet_loader.get_file_paths(reverse=True)
    total_files = len(file_paths)

    print(f"Starting processing {total_files} files...")

    with multiprocessing.Manager() as manager:
        counter = manager.Value('i', 0)
        progress_queue = manager.Queue()

        with ProcessPoolExecutor() as executor:
            results = list(
                executor.map(process_file, file_paths, [counter] * total_files, [progress_queue] * total_files)
            )
        while not progress_queue.empty():
            print(f"Progress: {progress_queue.get()} / {total_files} files processed")
    # 결과 병합
    final_counts = combine_results(results)

    # 결과 출력
    output_file = 'data_preview.txt'
    with open(output_file, 'w') as f:
        for category, counts in final_counts.items():
            f.write(f'{category}:\n')
            for value, count in sorted(counts.items()):
                f.write(f'  {value}: {count}\n')
