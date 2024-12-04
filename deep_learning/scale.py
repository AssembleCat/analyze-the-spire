import json
import os
from datetime import datetime

import numpy as np
from sklearn.preprocessing import MaxAbsScaler


def scale_data(features, labels):
    return scale_features(features), scale_labels(labels)


def scale_features(features):
    # 표준화
    sc = MaxAbsScaler()
    scaled_features = sc.fit_transform(features)
    # 결과 저장
    np.save("cache/scaled_x.npy", scaled_features)

    return scaled_features


def scale_labels(labels):
    label_copy = labels.copy()
    label_copy /= 100
    # 최대 회복, 데미지를 100으로 제한
    label_copy[label_copy < -1] = -1
    label_copy[label_copy > 1] = 1

    np.save("cache/scaled_y.npy", label_copy)

    return label_copy
