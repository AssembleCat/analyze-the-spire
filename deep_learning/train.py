import os
import numpy as np

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import datetime
import json
import tensorflow as tf
from sklearn.model_selection import train_test_split
from deep_learning import preprocess, scale

x, y = None, None

# cache 데이터 체크
cache_data = [file for file in os.listdir("./cache") if file.endswith(".npy")]
if cache_data:
    x, y = np.load("./cache/scaled_x.npy"), np.load("./cache/scaled_y.npy")
else:
    BATTLE_DATA = "../battles/clean/"
    json_files = [file for file in os.listdir(BATTLE_DATA) if file.endswith(".json")][:1]
    json_data = []

    for file in json_files:
        with open(BATTLE_DATA + file) as json_file:
            json_data.extend(json.load(json_file))

    print(f"Preprocess target battle: {len(json_data)}")

    x, y = preprocess.preprocess_battle(json_data)
    x, y = scale.scale_data(x, y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# embedded encoding = (86,), one-hot encoding = (982, )
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer(shape=(86,)),
    tf.keras.layers.Dense(500, activation='relu'),
    tf.keras.layers.Dropout(.2),
    tf.keras.layers.Dense(50, activation='relu'),
    tf.keras.layers.Dropout(.1),
    tf.keras.layers.Dense(1)
])

model.summary()
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=.001),
    loss=tf.keras.metrics.mae,
    metrics=[tf.keras.metrics.R2Score(), tf.keras.metrics.mse])

# 시각화 정보 저장
logdir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)

# 훈련
history = model.fit(x_train, y_train, batch_size=32, epochs=10, validation_split=0.2, callbacks=[tensorboard_callback])

# 평가
test_scores = model.evaluate(x_test, y_test, verbose=2)

print(f"""
Test loss: {test_scores[0]}
Test metric: {test_scores[1]}
""")

# 모델 저장
model.save("./model/analyze_the_spire.keras")
