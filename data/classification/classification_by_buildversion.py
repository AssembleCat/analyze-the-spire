import os
from pathlib import Path

import pandas as pd
from data import parquet_loader

OUTPUT_PATH = "C:/Users/groov/AnalyzeTheSpire/ClassifiedData"


# 데이터 파일 읽기 함수
def process_and_save_files(data_paths):
    current, end = 0, len(data_paths)
    for file in data_paths:
        current += 1
        print(f"({current}/{end}) Classifying {file}")
        try:
            # 파일 읽기
            df = pd.read_parquet(file)

            # "build_version" 열 확인
            if "build_version" not in df.columns:
                print(f"Skipping {file}: 'build_version' column not found.")
                return

            # build_version 값 확인
            unique_versions = df['build_version'].unique()

            for version in unique_versions:
                # 버전별 데이터 필터링
                filtered_df = df[df['build_version'] == version]

                # 버전별 폴더 경로 생성
                version_folder = os.path.join(OUTPUT_PATH, str(version))
                os.makedirs(version_folder, exist_ok=True)

                # 파일 이름 결정 및 저장
                output_file_path = os.path.join(version_folder, Path(file).stem + ".parquet")
                filtered_df.to_parquet(output_file_path)
                print(f"Saved data for version '{version}' to {output_file_path}")

        except Exception as e:
            print(f"Error processing {file}: {e}")


def rename_files_in_place(data_paths):
    folder_files = {}

    # 파일을 폴더별로 그룹화
    for path in data_paths:
        folder_path = os.path.dirname(path)  # 파일의 폴더 경로
        folder_name = os.path.basename(folder_path)  # 폴더 이름
        if folder_path not in folder_files:
            folder_files[folder_path] = []
        folder_files[folder_path].append((folder_name, path))

    # 파일 이름 변경
    for folder_path, files in folder_files.items():
        files.sort(key=lambda x: x[1])  # 원래 경로로 정렬
        for idx, (folder_name, original_path) in enumerate(files, start=1):
            new_name = f"{folder_name}_{idx}.parquet"  # 새 파일 이름
            new_path = os.path.join(folder_path, new_name)

            # 파일 이름 변경
            os.rename(original_path, new_path)
            print(f"Renamed: {original_path} -> {new_path}")


if __name__ == '__main__':
    data_paths = parquet_loader.get_file_paths(folder_type="ClassifiedData")
    rename_files_in_place(data_paths)
