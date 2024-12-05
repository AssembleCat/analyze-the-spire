import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import tensorflow as tf
from type import sts_static
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

ENCODE_EMBEDDED = True
card_encoder = LabelEncoder().fit(sts_static.ALL_CARDS)
relic_encoder = LabelEncoder().fit(sts_static.ALL_RELICS)
enemy_encoder = LabelEncoder().fit(sts_static.ALL_ENEMY)


def preprocess_battle(data):
    processed_battles, label = [], []

    for idx, battle in enumerate(data):
        if idx % 2000 == 0:
            print(f"{idx / len(data) * 100:.2f}% complete, {idx} in {len(data)}")

        label.append(battle["damage_taken"])

        if ENCODE_EMBEDDED:
            processed_battles.append(encode_embedded_battle(battle))
        else:
            processed_battles.append(encode_battle(battle))

    x = np.vstack(processed_battles)
    y = np.array(label, dtype='float32')

    return x, y


def encode_embedded_battle(battle):
    """
    embedding array로 변환 길이 = 86
    """
    card_encoded = card_encoder.transform(remove_basic_card_suffix(np.array(battle["deck"])))
    card_encoded += 1  # 0이 없도록 1 더해주기
    card_encoded = card_encoded.reshape(1, -1)  # 1개행으로 고정변환
    card_encoded = tf.keras.preprocessing.sequence.pad_sequences(card_encoded, maxlen=50, padding='post', truncating='post')

    relic_encoded = relic_encoder.transform(np.array(battle["relics"]))
    relic_encoded += 1
    relic_encoded = relic_encoded.reshape(1, -1)
    relic_encoded = tf.keras.preprocessing.sequence.pad_sequences(relic_encoded, maxlen=30, padding='post', truncating='post')

    enemy_encoded = enemy_encoder.transform([np.array(battle["enemy"])])
    enemy_encoded = enemy_encoded.reshape(1, -1)

    single_encoded = np.array([battle["max_hp"], battle["entering_hp"], battle["ascension"], battle["floor"], int(battle["potion_used"] is True)])

    return np.concatenate((card_encoded, relic_encoded, enemy_encoded, single_encoded), axis=None)


def encode_battle(battle):
    """
    단일 전투정보에 대해서 OneHotEncoding 결과를 반환. 길이 = 982

    :param battle: 단일 전투 정보
    :return from battle encoded np.array()
    """
    card_one_hot = one_hot_encode_count(remove_basic_card_suffix(battle["deck"]), sts_static.ALL_CARDS)
    relics_one_hot = one_hot_encode_count(battle["relics"], sts_static.ALL_RELICS)
    character_one_hot = one_hot_encode_single(battle["character"], sts_static.ALL_CHARACTERS)
    enemy_one_hot = one_hot_encode_single(battle["enemy"], sts_static.ALL_ENEMY)
    single_one_hot = np.array(
        [battle["max_hp"], battle["entering_hp"], battle["ascension"], battle["floor"], int(battle["potion_used"] is True)]
    )

    return np.concatenate([card_one_hot, relics_one_hot, character_one_hot, enemy_one_hot, single_one_hot])


def one_hot_encode_count(data, all_categories):
    """
    데이터의 빈도까지 포함하는 OneHotEncoding

    :param data: list: Battle 데이터를 포함한 리스트 (예: battle["cards"]).
    :param all_categories: list: 모든 가능한 카테고리 리스트 (예: sts_static.ALL_CARDS).
    :return np.array(): OneHotEncoded 결과를 담은 데이터프레임.
    """
    encoder = OneHotEncoder(categories=[all_categories], sparse_output=False)
    encode_target = np.array(data).reshape(len(data), 1)

    onehot_encoded = encoder.fit_transform(encode_target)

    return onehot_encoded.sum(axis=0)


def one_hot_encode_single(value, all_categories):
    """
    단일 값에 대해 OneHotEncoding 수행

    :param value: single value: Battle 데이터의 단일 항목 (예: battle["enemies"]).
    :param all_categories: list: 모든 가능한 카테고리 리스트 (예: sts_static.ALL_ENEMY).
    :return np.array(): OneHotEncoded 결과를 담은 데이터프레임.
    """
    encoder = OneHotEncoder(categories=[all_categories], sparse_output=False)
    encode_target = np.array([[value]])

    onehot_encoded = encoder.fit_transform(encode_target)

    return np.sum(onehot_encoded, axis=0)


def remove_basic_card_suffix(cards):
    """
    Strike, Defend 접미사를 제거

    :param cards: Battle 데이터를 포함한 리스트 (ex: battle["cards"]).
    :return upgraded_cards: 제공된 카드에 대해 업그레이드된 카드를 포함한 리스트.
    """
    for idx, card in enumerate(cards):
        if card.startswith("Strike_") or card.startswith("Defend_"):
            cards[idx] = card.split("_")[0]
    return cards
