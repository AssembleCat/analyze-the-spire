import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

from type import Character

characters = Character.get_character_list()
data_path = os.path.join(os.getcwd(), '..', 'data', 'processed')

df = pd.read_json(os.path.join(data_path, 'summary.json'))
x = df.drop('victory', axis=1)
y = df['victory']

correlation_matrix = x.corr()

plt.figure(figsize=(20, 20))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Feature Correlation Heatmap")
plt.show()

model = RandomForestClassifier(n_estimators=100, max_depth=10)
model.fit(x, y)

feat_importance = model.feature_importances_
feat_names = x.columns

feat_importance_df = pd.DataFrame({
    'Feature': feat_names,
    'Importance': feat_importance
})

feat_importance_df = feat_importance_df.sort_values(by='Importance', ascending=False)

print(feat_importance_df)