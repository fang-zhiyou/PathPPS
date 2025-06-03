import pandas as pd
import numpy as np

paths = ['Beijing', 'Chicago', 'Feicheng', 'Sparse1', 'Sparse2', 'Sparse3']

for p in paths:
    result_path = f'{p}.csv'
    df = pd.read_csv(result_path, encoding='utf-8', dtype={'PathPPS_len': int, 'PathPPS_time': float, 'Real_len': int, 'Acc': float})  # 指定列数据类型

    max_value = 4000
    min_value = 0

    n = 8
    bins = np.linspace(min_value, max_value, n + 1).astype(int)
    # print("分割点:", bins)
    # print("区间长度:", (max_value - min_value) / n)

    df['range'] = pd.cut(df['Real_len'], bins)
    result = df.groupby('range', observed=True).mean()

    text = result.to_string(index=True)
    with open('Exp_results.txt', 'a', encoding='utf-8') as file:
        file.write(f'{p} \n')
        file.write(f'{text} \n\n\n')
