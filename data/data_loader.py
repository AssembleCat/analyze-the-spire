import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from type import Character


def processed_data(data_name, data_type='processed', split=True, std=True):
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_type)

    df = pd.read_json(os.path.join(data_path, f'{data_name}.json'))
    x = df.drop('victory', axis=1)
    y = df['victory']

    x_train, x_test, y_train, y_test = None, None, None, None

    # 분할
    if split:
        x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, random_state=42)

    # 표준화
    if std:
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)

    return x_train, x_test, y_train, y_test
