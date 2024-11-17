from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

from data import data_loader

# 최적의 하이퍼파라미터:  {'estimator': DecisionTreeClassifier(max_depth=2, random_state=42), 'learning_rate': 1.0, 'n_estimators': 200}
# 최고 교차검증 점수:  0.9312589235477745

x_train, x_test, y_train, y_test = data_loader.processed_data('summary')

ada_boost = AdaBoostClassifier(algorithm='SAMME')

param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 1.0],
    'estimator': [
        DecisionTreeClassifier(max_depth=1, random_state=42),
        DecisionTreeClassifier(max_depth=2, random_state=42)
    ]
}

grid_search = GridSearchCV(
    estimator=ada_boost,
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