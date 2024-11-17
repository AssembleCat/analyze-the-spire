from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from data import data_loader

# 분할
x_train, x_test, y_train, y_test = data_loader.processed_data('summary')

# 표준화
sc = StandardScaler()
x_train_std = sc.fit_transform(x_train)
x_test_std = sc.transform(x_test)

# PCA 추출
pca = PCA(n_components=3)
pca.fit(x_train_std)

print(pca.explained_variance_ratio_)

x_train_std_pca = pca.transform(x_train_std)
x_test_std_pca = pca.transform(x_test_std)

logistic = LogisticRegression(max_iter=5000)
logistic_pca = LogisticRegression(max_iter=5000)

logistic.fit(x_train_std, y_train)
logistic_pca.fit(x_train_std_pca, y_train)

print(f"""
Logistic: {logistic.score(x_test_std, y_test):.3f}
Logistic_PCA: {logistic_pca.score(x_test_std_pca, y_test):.3f}
""")
