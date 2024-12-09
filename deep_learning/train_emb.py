import json
import os
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from deep_learning import preprocess, scale
from keras import Input, Model
from keras.src.layers import Embedding, Lambda, concatenate, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MaxAbsScaler
from type import sts_static


def load_data(character):
    X = np.load(f"./cache/{character}_x.npy")
    Y = np.load(f"./cache/{character}_y.npy")
    return X, Y


def avg_lambda_fun(x, mask):
    mask_cast = tf.keras.backend.cast(mask, 'float32')
    expanded = tf.keras.backend.expand_dims(mask_cast)
    count = tf.keras.backend.sum(mask_cast)
    sum = tf.keras.backend.sum(expanded * x, axis=1)
    return sum / count


def preprocess_data(character):
    x, y = None, None
    cache_data = [file for file in os.listdir("./cache") if file.endswith(".npy")]
    if f"{character}_x.npy" in cache_data:
        x, y = np.load(f"./cache/{character}_x.npy"), np.load(f"./cache/{character}_y.npy")
    else:
        BATTLE_DATA = f"../battles/clean/{character}/"
        json_files = [file for file in os.listdir(BATTLE_DATA) if file.endswith(".json")][:45]
        json_data = []

        print(f"total file length: {len(json_files)}")

        for file in json_files:
            with open(BATTLE_DATA + file) as json_file:
                json_data.extend(json.load(json_file))

        print(f"Preprocess target battle: {len(json_data)}")

        x, y = preprocess.preprocess_battle(json_data, character)
        x, y = scale.scale_data(x, y, character)

    return x, y


def create_embedding_layers(character):
    # 캐릭터별 카드풀
    character_card = sts_static.get_character_cardpool(character)

    # 카드 임베딩
    card_input = Input(shape=(50,), name='cards_input')
    card_embedding = Embedding(len(character_card) + 1, 26, mask_zero=True)(card_input)
    card_average = Lambda(avg_lambda_fun, output_shape=(26,), mask=None)(card_embedding)

    # 유물 임베딩
    relic_input = Input(shape=(30,), name='relics_input')
    relic_embedding = Embedding(len(sts_static.ALL_RELICS) + 1, 13, mask_zero=True)(relic_input)
    relic_average = Lambda(avg_lambda_fun, output_shape=(13,), mask=None)(relic_embedding)

    # 적 임베딩
    enemy_input = Input(shape=(1,), name='enemy_input')
    enemy_embedding = Embedding(len(sts_static.ALL_ENEMY), 8)(enemy_input)
    enemy_reshape = Lambda(lambda x: tf.keras.backend.mean(x, axis=1), output_shape=(8,))(enemy_embedding)

    # 숫자 및 부울 입력
    numbers_input = Input(shape=(5,), name='num_and_bool_input')

    return card_input, card_average, relic_input, relic_average, enemy_input, enemy_reshape, numbers_input


def build_model(card_average, relic_average, encounter_reshape, numbers_input):
    merged = concatenate([card_average, relic_average, encounter_reshape, numbers_input])
    dense_1 = Dense(500, activation='relu')(merged)
    drop_out_1 = Dropout(.2)(dense_1)
    dense_2 = Dense(50, activation='relu')(drop_out_1)
    drop_out_2 = Dropout(.2)(dense_2)
    dense_out = Dense(1)(drop_out_2)

    return dense_out


def split_data(X, Y):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, shuffle=False)

    cards_col, cards_col_test = X_train[:, 0:50], X_test[:, 0:50]
    relic_index = 50 + 30
    relics_col, relics_col_test = X_train[:, 50:80], X_test[:, 50:80]
    enemy_index = relic_index + 1
    enemy_col, enemy_col_test = X_train[:, relic_index:enemy_index], X_test[:, relic_index:enemy_index]
    num_and_bool_col, num_and_bool_col_test = X_train[:, enemy_index:], X_test[:, enemy_index:]

    # 정규화
    max_abs_scaler = MaxAbsScaler()
    num_and_bool_col = max_abs_scaler.fit_transform(num_and_bool_col)

    return cards_col, relics_col, enemy_col, num_and_bool_col, Y_train, cards_col_test, relics_col_test, enemy_col_test, num_and_bool_col_test, Y_test


def train_model(X, Y, character):
    # 데이터 준비
    cards_col, relics_col, enemy_col, num_and_bool_col, Y_train, cards_col_test, relics_col_test, enemy_col_test, num_and_bool_col_test, Y_test = split_data(
        X, Y)

    # 임베딩 레이어 생성
    card_input, card_average, relic_input, relic_average, encounter_input, encounter_reshape, numbers_input = create_embedding_layers(character)

    # 모델 생성
    dense_out = build_model(card_average, relic_average, encounter_reshape, numbers_input)
    model = Model(inputs=[card_input, relic_input, encounter_input, numbers_input], outputs=dense_out)
    model.summary()

    # 컴파일
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-4),
        loss='mse',
        metrics=['mae', tf.keras.metrics.R2Score()])

    # 훈련
    history = model.fit(
        x={
            'cards_input': cards_col,
            'relics_input': relics_col,
            'enemy_input': enemy_col,
            'num_and_bool_input': num_and_bool_col
        },
        y=Y_train,
        batch_size=32,
        epochs=5,
        validation_split=0.2
    )

    # 평가
    test_loss, test_mae, test_r2 = model.evaluate(
        x={
            'cards_input': cards_col_test,
            'relics_input': relics_col_test,
            'enemy_input': enemy_col_test,
            'num_and_bool_input': num_and_bool_col_test
        },
        y=Y_test
    )
    print(f"Test Loss: {test_loss}")
    print(f"Test MAE: {test_mae}")
    print(f"Test R² Score: {test_r2}")

    return model, history


if __name__ == "__main__":
    X, Y = preprocess_data('WATCHER')
    trained_model, training_history = train_model(X, Y, 'WATCHER')
