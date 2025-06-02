import numpy as np
import osmnx as ox
import geopandas as gpd
from geopy.distance import geodesic
from matplotlib import pyplot as plt


def calculate_density():
    def get_area(bbox):
        coord1 = (bbox[1], bbox[0])
        coord2 = (bbox[3], bbox[0])
        x = round(geodesic(coord1, coord2).meters, 0)
        coord1 = (bbox[3], bbox[2])
        y = round(geodesic(coord1, coord2).meters, 0)
        return x, y



    # 1. 定义自定义边界框 [minx, miny, maxx, maxy]
    bbox = (-119.59434, 39.74795, -119.54335, 39.78420) # 示例：北京某矩形区域
    # 2. 获取该范围内的路网数据
    graph = ox.graph.graph_from_bbox(bbox, network_type='drive')

    # 3. 转换为GeoDataFrame并计算
    gdf_edges = ox.graph_to_gdfs(graph, nodes=False)
    total_length = gdf_edges['length'].sum() / 1000 # km
    print(total_length)

    w, h = get_area(bbox)
    area = w * h / 1000000

    density = total_length / area
    print(density)
    print(f"自定义区域路网密度: {density:.2f} km/km²")


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




