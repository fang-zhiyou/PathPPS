import networkx as nx
import numpy as np
import osmnx as ox
from geopy.distance import geodesic


import cv2
from matplotlib import pyplot as plt

def image_split(image_path: str, rows, cols, percent):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    matrix2 = np.zeros((rows, cols), dtype=np.uint8)

    block_height = height // rows
    block_width = width // cols

    for i in range(rows):
        for j in range(cols):
            # 计算小图片的边界
            left = j * block_width
            upper = i * block_height
            right = left + block_width
            lower = upper + block_height

            # 裁剪小图片
            block = img[upper:lower, left:right]

            cnt = 0
            for row in block:
                for element in row:
                    if element > 64:
                        cnt += 1
            if cnt > percent * (block_width * block_height):
                matrix2[i, j] = 1

            # 保存小图片
            # cv2.imwrite(f"./{output_dir}/block_{i}_{j}.png", block)
    return matrix2


def plot_grid_road(mat2, save: bool, filepath: str):
    rows, cols = mat2.shape
    plt.figure(figsize=(cols * 0.3, rows * 0.3))

    for i in range(rows):
        for j in range(cols):
            if mat2[i, j] == 1:
                plt.fill_between([j, j+ 1], i, i + 1, facecolor='green', alpha=0.5)

    plt.xlim((0, cols))
    plt.ylim((rows, 0))

    plt.xticks(np.arange(0, cols, 1))
    plt.yticks(np.arange(0, rows, 1))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, linestyle='-', color='gray', alpha=0.7, zorder=0)
    plt.tight_layout()
    if save:
        plt.savefig(filepath)
        return
    plt.show()


def get_area(bbox):
    coord1 = (bbox[1], bbox[0])
    coord2 = (bbox[3], bbox[0])
    x = round(geodesic(coord1, coord2).meters, 0)
    coord1 = (bbox[3], bbox[2])
    y = round(geodesic(coord1, coord2).meters, 0)
    return x, y



if __name__ == '__main__':

    # 稠密地图
    # bboxBJ = (116.399827, 39.914378, 116.420972, 39.932243)
    # bboxChicago = (-87.806309, 41.875329, -87.761148, 41.909412) drive
    # bboxFC = (-75.185114, 39.916969, -75.154853, 39.940303)

    # 稀疏地图
    # bboxC1 = (118.90065, 35.30560, 118.95430, 35.33613)
    # bboxC2 = (-121.97047, 46.94288, -121.91563, 46.97539)
    # bboxC3 = (-119.59434, 39.74795, -119.54335, 39.78420)


    box = (-119.59434, 39.74795, -119.54335, 39.78420)
    box_name = 'Sparse3'

    G = ox.graph.graph_from_bbox(box, network_type="walk")
    print(f'{box_name}，节点数量： {G.number_of_nodes()}, 边数量：{G.number_of_edges()}')
    width, length = get_area(box)
    print(f'长度与宽度: {(width, length)}')

    # 重新编号并输出边信息
    mapping = {node: i for i, node in enumerate(G.nodes)}
    G_relabel = nx.relabel_nodes(G, mapping)
    with open(f'datasets/{box_name}.txt', 'w') as file:
        for u, v in G_relabel.edges():
            file.write(f'{u} {v}\n')

    # 计算稠密度
    gdf_edges = ox.graph_to_gdfs(G, nodes=False)
    total_length = gdf_edges['length'].sum() / 1000  # km
    w, h = get_area(box)
    area = w * h / 1000000
    density = total_length / area
    print(f"自定义区域路网密度: {density:.2f} km/km²")

    # img_path = f'datasets/{box_name}.png'
    # fig, ax = ox.plot.plot_graph(G, figsize=(20, 20), edge_color="w", edge_linewidth=4, save=True, filepath=img_path)
    #
    #
    # cell = 14 # 设置网格大小
    # w_cells = int(width) // cell
    # l_cells = int(length) // cell
    #
    # print("网格图生成中...")
    # matrix2 = image_split(img_path, w_cells, l_cells, percent=0.2)
    # np.save(f'datasets/{box_name}.npy', matrix2)
    #
    # print("网格图绘制中...")
    # grid_path = f'datasets/{box_name}_grid.png'
    # plot_grid_road(matrix2, save=True, filepath=grid_path)
    # print(f'网格数量：{w_cells * l_cells}')


# cell = 64

# CountrySide2，节点数量： 10, 边数量：18
# 长度与宽度: (3614.0, 4173.0)
# 1.13

# CountrySide1，节点数量： 35, 边数量：88
# 长度与宽度: (3387.0, 4877.0)
# 2.09

# CountrySide3，节点数量： 20, 边数量：42
# 长度与宽度: (4025.0, 4368.0)
#1.08

# Chicago
# 32  drive
# Chicago，节点数量： 908, 边数量：2562
# 长度与宽度: (3786.0, 3747.0)
# 自定义区域路网密度: 22.91 km/km²

# Feicheng
# 14 0.2 walk
# Feicheng，节点数量： 2490, 边数量：7858
# 长度与宽度: (2591.0, 2586.0)
# 自定义区域路网密度: 62.99 km/km²



# Beijing，节点数量： 602, 边数量：1690
# 长度与宽度: (1984.0, 1807.0)
# 自定义区域路网密度: 36.83 km/km²
# cell = 14 walk


