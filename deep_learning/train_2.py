import os
import numpy as np

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from keras import Input, Model
from keras.src.layers import Embedding, Lambda, concatenate, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MaxAbsScaler
from type import sts_static


def load_data():
    X = np.load("./cache/scaled_x.npy")
    Y = np.load("./cache/scaled_y.npy")
    return X, Y


def avg_lambda_fun(x, mask):
    mask_cast = tf.keras.backend.cast(mask, 'float32')
    expanded = tf.keras.backend.expand_dims(mask_cast)
    count = tf.keras.backend.sum(mask_cast)
    sum = tf.keras.backend.sum(expanded * x, axis=1)
    return sum / count


def create_embedding_layers():
    # 카드 임베딩
    card_input = Input(shape=(50,), name='cards_input')
    card_embedding = Embedding(len(sts_static.ALL_CARDS) + 1, 26, mask_zero=True)(card_input)
    card_average = Lambda(avg_lambda_fun, output_shape=(26,), mask=None)(card_embedding)

    # 유물 임베딩
    relic_input = Input(shape=(30,), name='relics_input')
    relic_embedding = Embedding(len(sts_static.ALL_RELICS) + 1, 13, mask_zero=True)(relic_input)
    relic_average = Lambda(avg_lambda_fun, output_shape=(13,), mask=None)(relic_embedding)

    # 적 임베딩
    encounter_input = Input(shape=(1,), name='encounter_input')
    encounter_embedding = Embedding(len(sts_static.ALL_ENEMY), 8)(encounter_input)
    encounter_reshape = Lambda(lambda x: tf.keras.backend.mean(x, axis=1), output_shape=(8,))(encounter_embedding)

    # 숫자 및 부울 입력
    numbers_input = Input(shape=(5,), name='num_and_bool_input')

    return card_input, card_average, relic_input, relic_average, encounter_input, encounter_reshape, numbers_input


def build_model(card_average, relic_average, encounter_reshape, numbers_input):
    merged = concatenate([card_average, relic_average, encounter_reshape, numbers_input])
    dense_1 = Dense(40, activation='relu')(merged)
    drop_out_1 = Dropout(.1)(dense_1)
    dense_out = Dense(1)(drop_out_1)

    return dense_out


def preprocess_data(X, Y):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, shuffle=False)

    cards_col = X_train[:, 0:50]
    relic_index = 50 + 30
    relics_col = X_train[:, 50:80]
    encounter_index = relic_index + 1
    encounter_col = X_train[:, relic_index:encounter_index]
    num_and_bool_col = X_train[:, encounter_index:]

    # 정규화
    max_abs_scaler = MaxAbsScaler()
    num_and_bool_col = max_abs_scaler.fit_transform(num_and_bool_col)

    return cards_col, relics_col, encounter_col, num_and_bool_col, Y_train, X_test, Y_test


def train_model(X, Y):
    # 데이터 준비
    cards_col, relics_col, encounter_col, num_and_bool_col, Y_train, _, _ = preprocess_data(X, Y)

    # 임베딩 레이어 생성
    card_input, card_average, relic_input, relic_average, encounter_input, encounter_reshape, numbers_input = create_embedding_layers()

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
            'encounter_input': encounter_col,
            'num_and_bool_input': num_and_bool_col
        },
        y=Y_train,
        batch_size=32,
        epochs=20,
        validation_split=0.2
    )

    return model, history


if __name__ == "__main__":
    X, Y = load_data()
    trained_model, training_history = train_model(X, Y)
