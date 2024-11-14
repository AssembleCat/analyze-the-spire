import os
import json


def create_json_file(file_path, data=None):
    if data is None:
        data = {}
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data


def append_json_file(file_path, data):
    with open(file_path, 'a') as json_file:
        json.dump(data, json_file, indent=4)


def update_json_file(file_path, key, value):
    data = read_json_file(file_path)
    data[key] = value
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def save_json(path, file_name, data):
    full_path = os.path.join(path, file_name)

    if os.path.exists(full_path):
        append_json_file(full_path, data)
    else:
        create_json_file(full_path, data)