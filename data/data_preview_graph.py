import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with open('json/FilteredData_data_preview.json') as f:
    preview_json = json.load(f)

# 1. 캐릭터 플레이 횟수
character_df = pd.DataFrame(list(preview_json.get('character_chosen').items()), columns=['Character', 'Count'])

plt.figure(figsize=(10, 6))
barplot = sns.barplot(data=character_df, x="Character", y="Count", hue='Character', palette=('#3498db', '#ec7063', '#58d68d', '#9b59b6'), legend=False)

# 각 라벨별 value 즉, count를 표현
for container in barplot.containers:
    barplot.bar_label(container, fmt='%d', label_type='edge', fontsize=10)

plt.title("Character Selection Counts", fontsize=16, weight="bold")
plt.xlabel("Character", fontsize=12)
plt.ylabel("Count", fontsize=12)

plt.savefig("img/character_selection_count.png")
plt.show()

# 2. 승천별 플레이 횟수
ascension_df = pd.DataFrame(list(preview_json.get('ascension_level').items()), columns=['Ascension Level', 'Count'])

plt.figure(figsize=(10, 6))
barplot = sns.barplot(data=ascension_df, x="Ascension Level", y="Count", palette=sns.color_palette("husl", 21))

plt.title("Ascension Counts", fontsize=16, weight="bold")
plt.xlabel("Ascension Level", fontsize=12)

plt.ylabel("Count", fontsize=12)

plt.savefig("img/ascension_count.png")
plt.show()

# 3. 도달층별 횟수
floor_df = pd.DataFrame(list(preview_json.get('floor_reached').items()), columns=['Floor Reached', 'Count'])

plt.figure(figsize=(20, 6))
barplot = sns.barplot(data=floor_df, x="Floor Reached", y="Count", palette=sns.color_palette("husl", 58))

plt.title("Floor Reached Count", fontsize=16, weight="bold")
plt.xlabel("Floor Reached", fontsize=12)

plt.ylabel("Count", fontsize=12)

plt.savefig("img/floor_count.png")
plt.show()
