import os

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from type import Character

CLASS_WEIGHT = {False: 1, True: 1}

characters = Character.get_character_list()
data_path = os.path.join(os.getcwd(), '..', 'data', 'processed')

df = pd.read_json(os.path.join(data_path, 'silent.json'))
x = df.drop('victory', axis=1)
y = df['victory']

models = [
    LogisticRegression(max_iter=5000, class_weight=CLASS_WEIGHT),
    RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight=CLASS_WEIGHT),
    AdaBoostClassifier(DecisionTreeClassifier(max_depth=1, class_weight=CLASS_WEIGHT), n_estimators=100, algorithm='SAMME', learning_rate=0.8)
]

x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size=0.2, random_state=42)

sc = StandardScaler()
x_train_std = sc.fit_transform(x_train)
x_test_std = sc.transform(x_test)

print(np.unique(y))

for model in models:
    # 훈련
    print(f"\n타겟 모델: {type(model).__name__}")
    model.fit(x_train_std, y_train)

    # 휸련데이터 정확도
    print(f"\n훈련데이터 정확도: {model.score(x_train_std, y_train):.3f}")

    # Cross-Validation
    cv_score = cross_val_score(model, x_train_std, y_train, cv=10)
    print(f"\nCross-Validation 점수: {np.round(cv_score, 3)}, 평균: {np.round(np.mean(cv_score), 3)}")

    # 예측
    y_pred_test = model.predict(x_test_std)
    report = classification_report(y_test, y_pred_test)
    print(f"\n분류평가: {report}")

    # 정오분류표 계산 및 출력
    conf_matrix = confusion_matrix(y_test, y_pred_test)
    print("\nConfusion Matrix:\n", conf_matrix)
