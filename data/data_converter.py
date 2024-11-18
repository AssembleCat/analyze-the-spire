import os

import pandas as pd

df = pd.read_parquet(os.path.join(os.getcwd(), 'all'))