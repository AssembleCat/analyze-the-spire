from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

from data import data_loader

# 최적의 하이퍼파라미터:  {'C': 10, 'penalty': 'l1', 'solver': 'saga'}
# 최고 교차검증 점수:  0.9284302119290186

x_train, x_test, y_train, y_test = data_loader.processed_data('summary')

logistic = LogisticRegression(max_iter=5000)

param_grid = {
    'C': [0.1, 1, 10, 100],                 # 정규화 강도 (작을수록 강한 규제)
    'penalty': ['l1', 'l2'],                # l1 = ridge, l2 = lasso
    'solver': ['saga'],                     # 최적화 알고리즘
}

grid_search = GridSearchCV(
    estimator=logistic,
    param_grid=param_grid,
    scoring='accuracy',
    cv=10,
    verbose=2,
    n_jobs=-1
)

grid_search.fit(x_train, y_train)

print("최적의 하이퍼파라미터: ", grid_search.best_params_)
print("최고 교차검증 점수: ", grid_search.best_score_)

best_model = grid_search.best_estimator_
y_pred = best_model.predict(x_test)
print("\n테스트 데이터 평가:\n")
print(classification_report(y_test, y_pred))
