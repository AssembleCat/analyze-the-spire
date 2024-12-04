import json
from datetime import datetime
from sklearn.preprocessing import MaxAbsScaler


def scale_features(features):
    # 표준화
    sc = MaxAbsScaler()
    scaled_features = sc.fit_transform(features)
    # 결과를 저장
    save_battle_cache(scaled_features.tolist(), f"feature_{datetime.now().strftime('%Y%m%d')}")

    return scaled_features


def scale_labels(labels):
    label_copy = labels.copy()
    label_copy /= 100
    # 최대 회복, 데미지를 100으로 제한
    label_copy[label_copy < -1] = -1
    label_copy[label_copy > 1] = 1

    return label_copy


def save_battle_cache(data, file_name):
    with open(f"../battles/cache/{file_name}.json", "w") as f:
        json.dump(data, f)
