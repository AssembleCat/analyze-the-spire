import numpy as np
import pandas as pd


# neow_bonus, neow_cost 결측치 제거하기
def replace_row(data):
    df = data.copy()

    missing_per_column = df.isnull().sum()
    print("missing row (per col):")
    print(missing_per_column)

    missing_columns = missing_per_column[missing_per_column > 0]
    print("Columns with missing values: ")
    print(missing_columns)

    origin_row = df.shape[0]
    print("Remove rows for missing values")
    print(f"0. origin: {origin_row}")

    df['neow_bonus'] = df['neow_bonus'].replace('', np.nan)
    df['neow_cost'] = df['neow_cost'].replace('', np.nan)

    df.dropna(subset=['neow_bonus', 'neow_cost'], inplace=True)

    step1_row = df.shape[0]

    print(f"1. drop neow missing value: {step1_row}")

    return df
