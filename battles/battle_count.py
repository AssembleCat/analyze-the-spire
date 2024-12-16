import os
import json

folder_path = "./clean/THE_SILENT"

row_counts = {}

for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if isinstance(data, list):
                row_count = len(data)
            else:
                row_count = 0

            # 파일 이름과 행(row) 수 저장
            row_counts[file_name] = row_count

for file_name, count in row_counts.items():
    print(f"{file_name}: {count} rows")

# 전체 row 합산
total_rows = sum(row_counts.values())
print(f"Total rows across all files: {total_rows}")
