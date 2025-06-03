import pandas as pd
import numpy as np


result_path = 'Sparse3.csv'
df = pd.read_csv(result_path, encoding='utf-8', dtype={'PathPPS_len': int, 'PathPPS_time': float, 'Real_len': int, 'Acc': float})  # 指定列数据类型

# min_value = df['Real_len'].min()
# max_value = df['Real_len'].max()
# print(f"值范围: {min_value} 到 {max_value}")

max_value = 4000
min_value = 0

n = 8
bins = np.linspace(min_value, max_value, n + 1).astype(int)
print("分割点:", bins)
print("每个区间的长度:", (max_value - min_value) / n)


df['range'] = pd.cut(df['Real_len'], bins)
result = df.groupby('range', observed=True).mean()
print(result)
