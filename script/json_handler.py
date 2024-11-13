import json


# JSON 파일 생성 및 데이터 추가
def create_json_file(file_path, data=None):
    if data is None:
        data = {}
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# JSON 파일 읽기
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data


# JSON 배열에 추가
def append_json_file(file_path, data):
    with open(file_path, 'a') as json_file:
        json.dump(data, json_file, indent=4)


# JSON 파일에서 정보 추가 또는 수정
def update_json_file(file_path, key, value):
    data = read_json_file(file_path)
    data[key] = value
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
