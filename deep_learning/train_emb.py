import json
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import numpy as np
import scale
from keras.src.utils import pad_sequences
from sklearn.model_selection import train_test_split
from keras import Input, Model
from keras.src.layers import Embedding, Flatten, Concatenate, Dense, Dropout
from sklearn.preprocessing import LabelEncoder, StandardScaler
from type import sts_static

CACHE_DIR = './cache'
MODEL_DIR = './model'
EMBEDDING_DIM_CARD = 50
EMBEDDING_DIM_RELIC = 30
EMBEDDING_DIM_ENEMY = 8


def load_battle_data(character, max_rows=None):
    """
    특정 캐릭터의 전투 데이터를 로드합니다.

    Parameters:
    - character (str): 데이터 폴더 내 캐릭터 이름
    - max_rows (int, optional): 로드할 최대 ROW 수. None이면 전체 로드

    Returns:
    - json_data (list): 로드된 데이터 리스트
    """
    BATTLE_DATA = f"../battles/clean/{character}/"
    json_files = [file for file in os.listdir(BATTLE_DATA) if file.endswith(".json")]
    json_data = []

    print(f"Total file count: {len(json_files)}")
    total_rows = 0

    for file in json_files:
        with open(BATTLE_DATA + file) as json_file:
            file_data = json.load(json_file)
            print(f"Load file: {file}")

            if max_rows is not None:  # max_rows가 지정되었을 경우
                remaining_rows = max_rows - total_rows
                if len(file_data) <= remaining_rows:
                    json_data.extend(file_data)
                    total_rows += len(file_data)
                else:
                    json_data.extend(file_data[:remaining_rows])
                    total_rows += remaining_rows
                    break  # 목표한 ROW 수에 도달하면 루프 종료
            else:  # max_rows가 None이면 전체로드
                json_data.extend(file_data)

    print(f"Loaded rows: {len(json_data)}")
    return json_data


def save_cache(character, deck_data, relic_data, enemy_data, etc_data, damage_taken, is_train=True):
    """
    캐시 데이터를 저장하는 함수.
    """
    # 캐시 파일 이름 결정
    if is_train:
        deck_cache = f"{character}_deck_data.npy"
        relic_cache = f"{character}_relic_data.npy"
        enemy_cache = f"{character}_enemy_data.npy"
        etc_cache = f"{character}_etc_data.npy"
        damage_cache = f"{character}_damage_cache.npy"
    else:
        deck_cache = f"{character}_deck_data_test.npy"
        relic_cache = f"{character}_relic_data_test.npy"
        enemy_cache = f"{character}_enemy_data_test.npy"
        etc_cache = f"{character}_etc_data_test.npy"
        damage_cache = f"{character}_damage_cache_test.npy"

    cache_file_path = os.path.join(CACHE_DIR, deck_cache)
    # 이미 캐시 파일이 존재하면 리턴
    if os.path.exists(cache_file_path):
        print(f"Cache already exists: {cache_file_path}")
        return

    # 데이터 저장
    np.save(os.path.join(CACHE_DIR, deck_cache), deck_data)
    np.save(os.path.join(CACHE_DIR, relic_cache), relic_data)
    np.save(os.path.join(CACHE_DIR, enemy_cache), enemy_data)
    np.save(os.path.join(CACHE_DIR, etc_cache), etc_data)
    np.save(os.path.join(CACHE_DIR, damage_cache), damage_taken)

    print(f"Cache saved to: {cache_file_path}")


def load_cache(character, is_train=True):
    """
    캐시 파일을 불러오는 함수.
    """
    # 캐시 파일 경로 설정
    if is_train:
        deck_cache = f"{character}_deck_data.npy"
        relic_cache = f"{character}_relic_data.npy"
        enemy_cache = f"{character}_enemy_data.npy"
        etc_cache = f"{character}_etc_data.npy"
        damage_cache = f"{character}_damage_cache.npy"
    else:
        deck_cache = f"{character}_deck_data_test.npy"
        relic_cache = f"{character}_relic_data_test.npy"
        enemy_cache = f"{character}_enemy_data_test.npy"
        etc_cache = f"{character}_etc_data_test.npy"
        damage_cache = f"{character}_damage_cache_test.npy"
    cache_file_path = os.path.join(CACHE_DIR, deck_cache)

    # 캐시 파일이 없으면 None을 반환
    if not os.path.exists(cache_file_path):
        print(f"Cache not found, processing data: {cache_file_path}")
        return None

    # 캐시 파일에서 데이터 로드
    deck_data = np.load(os.path.join(CACHE_DIR, deck_cache), allow_pickle=True)
    relic_data = np.load(os.path.join(CACHE_DIR, relic_cache), allow_pickle=True)
    enemy_data = np.load(os.path.join(CACHE_DIR, enemy_cache), allow_pickle=True)
    etc_data = np.load(os.path.join(CACHE_DIR, etc_cache), allow_pickle=True)
    damage_taken = np.load(os.path.join(CACHE_DIR, damage_cache), allow_pickle=True)

    return [deck_data, relic_data, enemy_data, etc_data], damage_taken


def preprocess_data(data, character, card_encoder, relic_encoder, enemy_encoder, is_train=True):
    """
    전투 데이터를 전처리하여 캐시에 저장하고, 이미 저장된 캐시가 있으면 로드하는 함수.
    """
    # 캐시 로드
    cached_data = load_cache(character, is_train)
    character_cardpool = sts_static.get_character_cardpool(character)
    if cached_data:
        x, y = cached_data
        return x, y

    deck_data = []
    relic_data = []
    enemy_data = []
    etc_data = []
    damage_taken = []

    for idx, battle in enumerate(data):
        if idx % 5000 == 0:
            print(f"{idx / len(data) * 100:.2f}% {idx + 1}/{len(data)} Processing... ")

        # 캐릭터 카드풀에 없는 카드는 사용하지 않도록함. -> 프리즘 조각
        if any(card not in character_cardpool for card in battle["deck"]):
            continue
        # 카드 덱 라벨 인코딩
        encoded_deck = card_encoder.transform(battle["deck"]).tolist()
        # 유물 라벨 인코딩
        encoded_relics = relic_encoder.transform(battle["relics"]).tolist()
        # 적 라벨 인코딩
        encoded_enemy = enemy_encoder.transform([battle["enemy"]])
        # 체력 정보
        etc_info = [battle["max_hp"], battle["entering_hp"], battle["potion_used"], battle["ascension"], battle["floor"]]

        # 각 데이터에 추가
        deck_data.append(encoded_deck)
        relic_data.append(encoded_relics)
        enemy_data.append(encoded_enemy)
        etc_data.append(etc_info)
        damage_taken.append(battle["damage_taken"])

    # 패딩 처리
    deck_data = pad_sequences(deck_data, padding='post', truncating='post', maxlen=50, dtype=np.int32)
    relic_data = pad_sequences(relic_data, padding='post', truncating='post', maxlen=30, dtype=np.int32)

    enemy_data = np.array(enemy_data, dtype=np.int32)
    etc_data = np.array(etc_data, dtype=np.float32)
    damage_taken = np.array(damage_taken, dtype=np.float32)

    # 데미지 스케일링
    damage_taken = scale.scale_labels(damage_taken)

    # 캐시 저장
    save_cache(character, deck_data, relic_data, enemy_data, etc_data, damage_taken, is_train)

    return [deck_data, relic_data, enemy_data, etc_data], damage_taken


character = "WATCHER"
character_cardpool = sts_static.get_character_cardpool(character)
card_encoder = LabelEncoder().fit(character_cardpool)
relic_encoder = LabelEncoder().fit(sts_static.ALL_RELICS)
enemy_encoder = LabelEncoder().fit(sts_static.ALL_ENEMY)

# 데이터 로드 및 분할
battles = load_battle_data(character, 10000000)
train_data, test_data = train_test_split(battles, test_size=0.2, random_state=42)

# 전처리(인코딩)
X_train, Y_train = preprocess_data(train_data, character, card_encoder, relic_encoder, enemy_encoder)
X_test, Y_test = preprocess_data(test_data, character, card_encoder, relic_encoder, enemy_encoder, is_train=False)

# input shape 정의
deck_input = Input(shape=(50,), dtype='int32', name='deck')
relic_input = Input(shape=(30,), dtype='int32', name='relics')
enemy_input = Input(shape=(1,), dtype='int32', name='enemy')
etc_input = Input(shape=(5,), dtype='float32', name='etc')

# 카드 임베딩
card_embedding_layer = Embedding(input_dim=len(character_cardpool), output_dim=EMBEDDING_DIM_CARD)
embedded_deck = card_embedding_layer(deck_input)
embedded_deck = Flatten()(embedded_deck)

# 유물 임베딩
relic_embedding_layer = Embedding(input_dim=len(sts_static.ALL_RELICS), output_dim=EMBEDDING_DIM_RELIC)
embedded_relics = relic_embedding_layer(relic_input)
embedded_relics = Flatten()(embedded_relics)

# 적 임베딩
enemy_embedding_layer = Embedding(input_dim=len(sts_static.ALL_ENEMY), output_dim=EMBEDDING_DIM_ENEMY)
embedded_enemy = enemy_embedding_layer(enemy_input)
embedded_enemy = Flatten()(embedded_enemy)

# 결합
merged = Concatenate()([embedded_deck, embedded_relics, embedded_enemy, etc_input])

dense1 = Dense(500, activation='relu')(merged)
dropout1 = Dropout(0.2)(dense1)
dense2 = Dense(50, activation='relu')(dropout1)
dropout2 = Dropout(0.2)(dense2)
output = Dense(1, activation='linear')(dropout2)

# 모델 정의 및 컴파일
model = Model(inputs=[deck_input, relic_input, enemy_input, etc_input], outputs=output)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4), loss=tf.keras.metrics.mse, metrics=[tf.keras.metrics.R2Score()])

# 모델 요약
model.summary()

# 모델 학습
history = model.fit(
    X_train,
    Y_train,
    epochs=5,
    batch_size=32,
    validation_split=0.2
)

# 테스트셋 평가
test_loss = model.evaluate(X_test, Y_test)
print(f"Test loss: {test_loss}")

# 모델 저장
model.save(f'{character}.keras', save_format='keras')

# 히스토리 저장
with open(f'./history/{character}_history.json', 'w') as f:
    json.dump(history.history, f)
