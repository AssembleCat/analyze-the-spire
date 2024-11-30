import os
import re
from datetime import datetime

PATTERN = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
START_BUILD_VERSION, END_BUILD_VERSION = "2019-01-23", "2020-11-30"


def get_file_paths(root_path='default', reverse=False, folder_type='FilteredData'):
    """
    Get all .parquet file paths in the root folder, sorted by year, month, and file name.

    Args:
        root_path (str): The root directory containing the files.

    Returns:
        list: A list of sorted .parquet file paths.
        :param folder_type: folder type('Compressed', 'Filtered')
        :param root_path: root folder path
        :param reverse: default is False, but if True is given, the most recent data is returned.
    """
    if root_path == 'default':
        root_path = 'C:/Users/groov/AnalyzeTheSpire'

    root_path = os.path.join(root_path, folder_type)
    file_paths = []

    if folder_type == "ClassifiedData":
        for folder_name in os.listdir(root_path):
            # yyyy-MM-dd 폴더 이름인지 검사
            if not re.match(PATTERN, folder_name):
                print(f"{folder_name} is not a valid folder name")
                continue

            # 폴더이름, 빌드 시작/끝 변환
            folder_date = datetime.strptime(folder_name, "%Y-%m-%d")
            start_date = datetime.strptime(START_BUILD_VERSION, "%Y-%m-%d")
            end_date = datetime.strptime(END_BUILD_VERSION, "%Y-%m-%d")

            # 타켓 빌드버전 폴더 아래의 모든 데이터에 대한 경로를 추출
            if start_date <= folder_date < end_date:
                folder_path = os.path.join(root_path, folder_name)
                for dir_path, _, filenames in os.walk(folder_path):
                    for filename in filenames:
                        file_paths.append(os.path.join(dir_path, filename))

        return file_paths

    for year in sorted(os.listdir(root_path), reverse=reverse):
        year_path = os.path.join(root_path, year)
        if os.path.isdir(year_path):
            for month in sorted(os.listdir(year_path), reverse=reverse):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path):
                    for file in sorted(os.listdir(month_path), reverse=reverse):
                        if file.endswith('.parquet'):
                            file_paths.append(os.path.join(month_path, file))
    return file_paths


if __name__ == "__main__":
    root_folder_path = input("Enter the root folder path: ").strip()

    if os.path.exists(root_folder_path):
        parquet_paths = get_file_paths(root_folder_path)
        print(f"Found .parquet files: {len(parquet_paths)} count")
        for path in parquet_paths:
            print(path)
    else:
        print("Invalid root folder path. Check and try again.")
