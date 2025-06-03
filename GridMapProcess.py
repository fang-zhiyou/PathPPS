import numpy as np
import osmnx as ox
import geopandas as gpd
from geopy.distance import geodesic
from matplotlib import pyplot as plt


import cv2


# 读取文件，输出图片


def gen_pixel(filename: str):
    datapath_pre = f'datasets/{filename}.npy'

    dataset = np.load(datapath_pre)
    result = np.where(dataset == 0, 255, 0)
    cv2.imwrite(f'{filename}.png', result)


def process_pixel(filename: str):
    pic_path = f'{filename}.png'
    img = cv2.imread(pic_path, cv2.IMREAD_GRAYSCALE)
    result = np.where(img > 128, 255, 0)

    unique_values, counts = np.unique(result, return_counts=True)
    print("唯一值:", unique_values)
    print("出现次数:", counts)

    np.save(f'prodataset/{filename}.npy', result)

    rows, cols = result.shape
    plt.figure(figsize=(cols * 0.3, rows * 0.3))

    for i in range(rows):
        for j in range(cols):
            if result[i, j] == 0:
                plt.fill_between([j, j + 1], i, i + 1, facecolor='green', alpha=0.5)
    plt.xlim((0, cols))
    plt.ylim((rows, 0))
    plt.xticks(np.arange(0, cols, 1))
    plt.yticks(np.arange(0, rows, 1))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, linestyle='-', color='gray', alpha=0.7, zorder=0)
    plt.tight_layout()
    plt.savefig(f'prodataset/{filename}.png')


filename = 'CountrySide3'

# 基于 numpy 生成 图像
gen_pixel(filename)

# 优化图像
process_pixel(filename)




