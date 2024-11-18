import os
import pandas as pd
import category_encoders as ce

target_folder = os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'crawler', '20241113-230415'))

file_clear = pd.read_json(os.path.join(target_folder, f'silent_clear.json'))
file_fail = pd.read_json(os.path.join(target_folder, f'silent_fail.json'))
df = pd.concat([file_clear, file_fail])

encoder = ce.TargetEncoder(cols=['neow_bonus'])
df['neow_bonus_encoded'] = encoder.fit_transform(df['neow_bonus'], df['victory'])

# 변환된 데이터 확인
print(df[['neow_bonus', 'neow_bonus_encoded', 'victory']].head())