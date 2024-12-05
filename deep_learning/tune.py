import os
import numpy as np
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

model = tf.keras.models.load_model('./model/analyze_the_spire.h5')
x, y = np.load("./cache/scaled_x.npy"), np.load("./cache/scaled_y.npy")

print(model.evaluate(x, y, verbose=2))
