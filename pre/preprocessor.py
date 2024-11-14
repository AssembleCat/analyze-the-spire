import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def create_and_drop_feature(df, new_col_name, col1, col2, operation):
    df[new_col_name] = operation(df[col1], df[col2])

    df.drop([col1, col2], axis=1, inplace=True)
    return df


def categorical_encoding(col):
    encoder = LabelEncoder()
    return encoder.fit_transform(col)


def extract_boss_relics(boss_relics):
    act1_boss_relic = None
    act2_boss_relic = None

    for relic in boss_relics:
        if relic.get("act") == 1:
            act1_boss_relic = relic.get("picked", None)
        elif relic.get("act") == 2:
            act2_boss_relic = relic.get("picked", None)

    return pd.Series([act1_boss_relic, act2_boss_relic])


def calculate_average_damage(damage_taken, floor_reached):
    total_damage = sum(item['damage'] for item in damage_taken)

    if floor_reached > 0:
        average_damage = total_damage / floor_reached
    else:
        average_damage = np.nan  # floor_reached가 0일 경우, NaN으로 처리

    return average_damage


def count_items_purchased(items):
    card_count = sum(1 for item in items if item.get("is_card", False))
    relic_count = sum(1 for item in items if item.get("is_relic", False))
    potion_count = sum(1 for item in items if item.get("is_potion", False))

    return pd.Series([card_count, relic_count, potion_count])


def count_path_taken(paths):
    monster_count = sum(1 for path in paths if path == "M")
    unknown_count = sum(1 for path in paths if path == "?")
    store_count = sum(1 for path in paths if path == "$")
    elite_count = sum(1 for path in paths if path == "E")

    return pd.Series([monster_count, unknown_count, store_count, elite_count])


def run(df):
    # 여러 특성을 함께 계산하거나 특성이 확장되는 케이스
    df[['act1_boss_relic', 'act2_boss_relic']] = df['boss_relics'].apply(extract_boss_relics)
    df['average_damage_taken'] = df.apply(lambda x: calculate_average_damage(x['damage_taken'], x['floor_reached']), axis=1)
    df['gold_usage'] = df.apply(lambda x: x['gold_earned'] - x['gold'], axis=1)
    df[['card_purchased_count', 'relic_purchased_count', 'potion_purchased_count']] = df['items_purchased'].apply(count_items_purchased)
    df[['monster_count', 'unknown_event_count', 'store_count', 'elite_count']] = df['path_taken'].apply(count_path_taken)

    # 단일특성으로 연산가능한 경우
    preprocessing_rules = {
        'act1_boss_relic': categorical_encoding,
        'act2_boss_relic': categorical_encoding,
        'campfire_rested': lambda x: x,
        'campfire_upgraded': lambda x: x,
        'neow_bonus': categorical_encoding,
        'neow_cost': categorical_encoding,
        'potions_obtained': lambda x: x.apply(lambda y: len(y)),
        'purchased_purges': lambda x: x,
        'relics': lambda x: x.apply(lambda y: len(y)),
        'victory': lambda x: x
    }

    for col, func in preprocessing_rules.items():
        if isinstance(func, list):
            for f in func:
                df[col] = f(df[col])
        else:
            df[col] = func(df[col])

    # 전처리 후 특성 삭제
    drop_features = ['boss_relics', 'damage_taken', 'floor_reached', 'gold', 'gold_earned', 'items_purchased', 'path_taken']
    df.drop(columns=drop_features, inplace=True)

    return df
