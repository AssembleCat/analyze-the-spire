from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from data import data_loader


# 최적의 하이퍼파라미터:  {'class_weight': None, 'max_depth': None}
# 최고 교차검증 점수:  0.9255653177882983

x_train, x_test, y_train, y_test = data_loader.processed_data('summary')

random_forest = RandomForestClassifier(n_estimators=200)

param_grid = {
    'max_depth': [None, 5, 10, 20],
    'class_weight': [None, 'balanced_subsample']
}

grid_search = GridSearchCV(
    estimator=random_forest,
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
