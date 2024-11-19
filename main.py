import pandas as pd
from data import parquet_loader

file_path = parquet_loader.get_file_paths(reverse=True)[:1]

df_parquet = pd.read_parquet(file_path, engine='fastparquet')

print(df_parquet.info(verbose=True, memory_usage='deep'))
print(df_parquet.memory_usage())
